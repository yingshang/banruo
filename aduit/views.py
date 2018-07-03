# coding: utf-8
from django.shortcuts import render
from django.http import  JsonResponse,HttpResponseRedirect
from django.http.response import HttpResponse
from .models import proj_info,vul_info,setting,chandao_data,chandao_person_info
import time,datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  login as auth_login
from django.contrib.auth import authenticate
import calendar
from django.db.models import Count
from django.db.models import Q
from .fortify_run import push,git_api
from banruo.config import *
from .info import information
import hashlib
import pymysql
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from celery.decorators import task


def base(request):
    return  render(request,"base.html",locals())

def index(request):
    return render(request,'index.html',locals())



def save_setting(request):
    fortify_path = request.POST.get("fortify_path")
    report_path = request.POST.get("report_path")
    print(report_path)
    try:
        setting.objects.create(key="fortify_path",value=fortify_path)
    except:
        setting.objects.filter(key="fortify_path").update(value=fortify_path)
    try:
        setting.objects.create(key="report_path",value=report_path)
    except:
        setting.objects.filter(key="report_path").update(value=report_path)
    return JsonResponse({"status":1,"message":"save success!"})

def display_project(request):
    keyword = request.GET.get("keyword")
    try:
        page = int(request.GET.get("page")) or 1
    except:
        page = 1
    print(page)
    try:
        limit = int(request.GET.get("limit")) or 10
    except:
        limit = 10

    start = (page - 1) * limit
    end = page * limit
    if keyword == None:
        results = proj_info.objects.all()[start:end]
        project_count = proj_info.objects.all().count()


    else:
        results = proj_info.objects.filter(name__icontains=keyword)[start:end]
        project_count = proj_info.objects.filter(name__icontains=keyword).count()
    return render(request,"aduit/projects.html",locals())

def project_info(request):
    token = request.GET.get("token")
    id = request.GET.get('id')
    proj = proj_info.objects.get(token=token)
    risks = vul_info.objects.filter(proj_id=id).values('risk').annotate(Count('risk'))
    low_risk = 0
    Medium_risk = 0
    High_risk = 0
    Critical_risk = 0
    for i in range(len(risks)):
        if risks[i]['risk'] == 'Low':
            low_risk = risks[i]['risk__count']
        if risks[i]['risk'] == 'Medium':
            Medium_risk = risks[i]['risk__count']
        if risks[i]['risk'] == 'High':
            High_risk = risks[i]['risk__count']
        if risks[i]['risk'] == 'Critical':
            Critical_risk = risks[i]['risk__count']
    vuls = vul_info.objects.values('title').annotate(Count('title'))  # 所有漏洞标题
    critical_title = vul_info.objects.filter(proj_id=id).filter(Q(risk='Critical') | Q(risk='High')).values('title').annotate(Count('title'))  # 严重和高危漏洞标题
    # vul_title = vul_info.objects.filter(proj_id=id).values('title').annotate(Count('title'))  # 所有漏洞标题
    return render(request,"aduit/info.html",locals())

@csrf_exempt
def list(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        results = vul_info.objects.filter(proj_id=id)
        r = vul_info.objects.values('title').distinct()
        rule_filter = []
        for i in r:
            rule_filter.append(i['title'])
        vul_information = []
        for vul in results:
            vul_information.append({
                'line_number':vul.LineStart,
                'file_path':vul.FilePath,
                'level':vul.risk,
                'rule_name':vul.title,
                'language':vul.extend,
                'describe':information(vul.title)['describe'],
                'Recommendation':information(vul.title)['Recommendation'],
            })

        return JsonResponse({
            'code': 1001,
            'result': {
                'scan_data': {'extension': 21,
                              'language': 'php',
                              'trigger_rules': 12,
                              'vulnerabilities': vul_information,
                              'target_directory': '',
                              'push_rules': 12,
                              'framework': 'unkonw',
                              'file': 213
                              },
                'rule_filter': rule_filter,
            }},safe=False)
    else:
        return HttpResponse('must be post method ')

@csrf_exempt
def detail(request):
    id = request.POST.get('id')
    vid = request.POST.get('vid')
    print(vul_info.objects.filter(proj_id=id))
    code = vul_info.objects.filter(proj_id=id).get(vid=vid).full_code
    extend = vul_info.objects.filter(proj_id=id).get(vid=vid).extend
    return JsonResponse({
        'code':1001,
        'result':{
            'file_content':code,
            'extension':extend,
        }
    })

@csrf_exempt
def api_start(request):
    token = request.POST.get('id')
    git_url = proj_info.objects.get(id=id).git
    start(git_url)
    return JsonResponse({
        'code':1001,
        'result':'新增成功'
    })

@csrf_exempt
def api_proj_del(request):
    ids = request.POST.getlist('ids')
    for id in ids:
        vul_info.objects.filter(proj_id=id).delete()
        proj_info.objects.filter(id=id).delete()

    return JsonResponse({
        'code': 1001,
        'msg': '删除成功'
    })

@csrf_exempt
def api_chandao_del(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids')
        for id in ids:
            try:
                obj = chandao_data.objects.get(id=id)
                obj.hidden = 1
                obj.save()
            except:
                return  JsonResponse({
                    "code":1002,
                    "msg":"传入内容错误"
                })
        return JsonResponse({
            'code': 1001,
            'msg': '隐藏成功'
        })
    else:
        return JsonResponse({
            'code':1000,
            'msg':'必须使用POST方式'
        })

def overview(request):
    t = request.GET.get("t")
    if t =="week":
        dates = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        totals = []
        Week = datetime.datetime.now().isoweekday()
        time1 = datetime.date.today() - datetime.timedelta(days=Week-1)
        time2 = time1+datetime.timedelta(days=6)
        for i in range(Week):
            day = datetime.date.today() - datetime.timedelta(days=Week-2-i)
            day1 = datetime.date.today() - datetime.timedelta(days=Week-i-1)
            obj = proj_info.objects.filter(time__range=(day1,day))
            if obj:
                total = 0
                for i in obj:
                    total = total + int(i.total)
                totals.append(total)
            else:
                totals.append(0)
        critical_title = vul_info.objects.filter(time__range=(time1, time2)).filter(
            Q(risk='Critical') | Q(risk='High')).values('title').annotate(Count('title'))

    elif t=="month":
        dates = []
        now = datetime.date.today()
        year = now.year
        month = now.month
        totals = []
        day = calendar.monthrange(2018, 5)[1]
        for i in range(1,day):
            dates.append(i)
            try:
                obj = proj_info.objects.filter(time__range=(str(year)+"-"+str(month)+"-"+str(i),str(year)+"-"+str(month)+"-"+str(i+1)))
            except:
                t1 = str(year) + "-" + str(month) + "-" + str(i)
                t2 = str(year) + "-" + str(month+1) + "-1"
                obj = proj_info.objects.filter(time__range=(t1
                , t2))
            if obj:
                total = 0
                for i in obj:
                    total = total + int(i.total)
                totals.append(total)
            else:
                totals.append(0)

        time1 = datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(year)+'-'+str(month)+'-1', "%Y-%m-%d")))
        time2 = datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(year) + '-' + str(month) + '-' + str(day-1), "%Y-%m-%d")))
        critical_title = vul_info.objects.filter(time__range=(time1,time2 )).filter(
            Q(risk='Critical') | Q(risk='High')).values('title').annotate(Count('title'))
    elif t == "year":
        dates = []
        now = datetime.date.today()
        year = now.year
        month = now.month
        totals = []
        for i in range(1,13):
            dates.append(str(i)+"月")
            try:
                obj = proj_info.objects.filter(time__range=(str(year) + "-" + str(i) + "-1", str(year) + "-" + str(i+1) + "-1"))
            except:
                obj = proj_info.objects.filter(time__range=(str(year) + "-" + str(i) + "-1", str(year+1) + "-1-1"))
            if obj:
                total = 0
                for i in obj:
                    total = total + int(i.total)
                totals.append(total)
            else:
                totals.append(0)
        time1 = datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(year) + '-1-1', "%Y-%m-%d")))
        time2 = datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(year) + '-12-30', "%Y-%m-%d")))
        critical_title = vul_info.objects.filter(time__range=(time1, time2)).filter(
            Q(risk='Critical') | Q(risk='High')).values('title').annotate(Count('title'))
    else:
        pass
    return render(request,"aduit/overview.html",locals())

@csrf_exempt
def scan(request):
    if request.method == 'POST':
        t = request.POST.get('type')#1为git,2为git-list,3为SVN,4为上传
        if (t == "1"):
            gitaddress = request.POST.get("git_address")
            gitaccount = request.POST.get("git_username")
            gitpwd = request.POST.get("git_password")

            if len(gitaccount) == 0 and len(gitpwd) == 0:
                push.delay(gitaddress=gitaddress)
                return JsonResponse({"code":1001,"msg":"开始扫描"})
            else:
                if "https://" in gitaddress:
                    tmp = "https://" + gitaccount.replace("@", "%40") + ":" + gitpwd + "@"
                    address = gitaddress.replace("https://", tmp)
                    push.delay(gitaddress=address)
                elif "http://" in gitaddress:
                    tmp = "http://" + gitaccount.replace("@", "%40") + ":" + gitpwd + "@"
                    address = gitaddress.replace('http://', tmp)
                    push.delay(gitaddress=address)
                else:
                    pass
        elif(t == "2"):
            git_api()
            return  JsonResponse({"code":1001,"msg":"开始扫描!!!"})
        elif(t=="3"):
            svnaddress = request.POST.get("svn_address")
            svnaccount = request.POST.get("svn_username")
            svnpwd = request.POST.get("svn_password")
            push.delay(svnaddrss=svnaddress,type=3,svnaccount=svnaccount,svnpwd=svnpwd)
            return JsonResponse({"status":0,"msg":"开始扫描!!!"})
        elif(t=="4"):
            myFile = request.FILES.get("file", None)
            name = myFile.name
            if not myFile:
                return JsonResponse({"status":0,"msg":"上传失败!!!"})
            elif myFile.name.split('.')[1] != 'zip':
                return JsonResponse({"status":2,"msg":"上传文件必须为ZIP!!!"})
            else:
                destination = open(os.path.join("/data/fortify/", myFile.name), 'wb+')
                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()
                print(name)
                os.system("unzip -o  /data/fortify/" + myFile.name + "  -d  /data/fortify/")
                push.delay(name=name.split('.')[0],type=4)
                return JsonResponse({"status":1,"msg":"上传成功!!!"})

        else:
            return JsonResponse({"status":0,"msg":"参数类型错误"})

    else:
        address = git_api_adress
        p = parm
        choice = git_api_choice
        filepath = git_filepath
        return render(request,"aduit/scan.html",locals())

@csrf_exempt
def restart(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            type = proj_info.objects.get(id=id).type
            if type==1:
                git = proj_info.objects.get(id=id).git
                push.delay(gitaddress=git)

            elif type==3:
                svn = proj_info.objects.get(id=id).svn
                push.delay(svnaddress=svn)
            elif type ==4:
                return JsonResponse({"code":8888,"msg":"该项目是压缩上传，请重新上传压缩文件进行扫描"})
            else:
                return JsonResponse({"code":9999,"msg":"项目类型未知，无法重新扫描。"})

        except:
            return JsonResponse({"code":1000,"msg":"内容错误！！！"})
        return JsonResponse({"code":1001,"msg":"开始扫描!!!"})
    else:
        return JsonResponse({"code":1111,"msg":"请求方式必须为POST!!!"})

def chandao(request):
    keyword = request.GET.get("keyword")
    try:
        page = int(request.GET.get("page")) or 1
    except:
        page = 1
    print(page)
    try:
        limit = int(request.GET.get("limit")) or 10
    except:
        limit = 10

    start = (page-1)*limit
    end = page * limit
    if keyword == None:
        results = chandao_data.objects.all().exclude(hidden=1)[start:end]
        vul_count = chandao_data.objects.all().exclude(hidden=1).count()

    else:
        results = chandao_data.objects.filter(vul_name__icontains=keyword).exclude(hidden=1)[start:end]
        vul_count = chandao_data.objects.filter(vul_name__icontains=keyword).exclude(hidden=1).count()

    return render(request,"aduit/chandao.html",locals())


def filter_vul(request):
    results = vul_info.objects.all()
    for i in results:
        if i.risk =='Critical':
            if any(t  in i.title for t in filter_title):
                m = i.title.replace('\n','')+i.FileName.replace('\n','')+i.LineStart.replace('\n','')+i.FilePath.replace('\n','') #md5的明文
                md5 = hashlib.md5()
                md5.update(m.encode("utf8"))
                md5 = md5.hexdigest()
                vul_name = i.title
                FilePath = i.FilePath
                Abstract = i.Abstract
                FileName = i.FileName
                LineStart = i.LineStart
                info = information(vul_name)
                describe = info['describe']
                Recommendation = info['Recommendation']
                proj_name = proj_info.objects.get(id=i.proj_id.id).name
                if len(chandao_data.objects.filter(md5=md5)) == 0:
                    chandao_data.objects.create(
                                                md5=md5,
                                                vul_name = vul_name,
                                                FilePath = FilePath,
                                                Abstract = Abstract,
                                                FileName = FileName,
                                                describe = describe,
                                                Recommendation = Recommendation,
                                                LineStart = LineStart,
                                                proj_name = proj_name,
                                                )
    return JsonResponse({"code":1001,"msg":"过滤漏洞成功"})



def send_chandao(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    results = chandao_data.objects.all()
    for i in results:
        if i.status == 0:
            if i.hidden ==0:
                cinfo = chandao_person_info.objects.get(ename=i.proj_name)
                title = i.proj_name.strip()+'_'+i.vul_name.strip()
                #describe = cgi.escape(i.describe)
                #Recommendation = cgi.escape(i.Recommendation)
                project = cinfo.pid
                header = cinfo.header
                openedDate = now_time  # 创建时间
                assignedDate = now_time  # 指派时间
                contend = u'''
                <p><strong><span style="color:#E53333;">漏洞MD5：</span>%s</strong></p><p><b>
                <span style="color:#E53333;">产生漏洞的原因：</span>%s</b></p><p><b>
                <span style="color:#E53333;">漏洞文件名：</span>%s</b></p><p><b>
                <span style="color:#E53333;">漏洞位置：</span>%s</b></p><p><b>
                <span style="color:#E53333;">漏洞影响行：</span>%s</b></p><p><b>
                <span style="color:#E53333;">漏洞描述</span><span style="color:#E53333;">：</span></b></p>
                <pre>%s</pre><div><b><br> </b></div><b>
                <span style="color:#E53333;"></span><span style="color:#E53333;">
                </span><span style="color:#E53333;">
                </span><span style="color:#E53333;">
                </span><span style="color:#E53333;">漏洞修复方式：</span></b><p><br></p><p>
                <pre>%s</pre></p><p><br></p>
                ''' %(i.md5,i.Abstract,i.FileName,i.FilePath,i.LineStart,i.describe,i.Recommendation)
                conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DATABASE, port=MYSQL_PORT,charset="utf8")
                cursor = conn.cursor()
                sql = "SELECT * from zt_user where realname = '%s'" % header
                cursor.execute(sql)
                try:
                    header = cursor.fetchall()[0][2]
                except IndexError:
                    pass
                sql = "select id from zt_module where name='%s'" %i.proj_name
                cursor.execute(sql)
                module =cursor.fetchall()[0][0]
                # 插入禅道bug
                sql = "INSERT INTO `zt_bug` SET `product` = % s,`module` = 0,`hardware` = '1',`lastEditedDate` = '0000-00-00 00:00:00'," \
                      "`linkBug` = '1',`resolvedDate` = '0000-00-00 00:00:00',`activatedCount` = '0',`closedDate` = '0000-00-00 00:00:00'," \
                      "`duplicateBug` = '0',`project` = % s,`openedBuild` = 'trunk',`assignedTo` = % s,`mailto` = '',`type` = 'security'," \
                      "`os` = '',`browser` = '',`color` = '',`title` = % s,`severity` = '4',`pri` = '4',`steps` = % s,`story` = '0',`task` = '0'," \
                      "`keywords` = '',`case` = '0',`caseVersion` = '0',`result` = '0',`testtask` = '0',`openedBy` = % s,`openedDate` = % s," \
                      "`assignedDate` = % s;"
                cursor.execute(sql, (str(product),str(project),header, title, contend, openedBy, openedDate, assignedDate))
                bug_id = int(conn.insert_id())  # 最新插入行的主键ID
                conn.commit()
                # 关联bug表的更新
                sql2 = "INSERT INTO `zt_action` SET `objectType` = 'security',`objectID` = %s,`actor` = %s,`action` = 'opened'," \
                       "`date` = '0000-00-00 00:00:00',`comment` = '',`extra` = '',`product` = ',3,',`project` = %s" % (
                           bug_id, openedBy,project)
                cursor.execute(sql2)
                conn.commit()
                cursor.close()
                i.status=1
                i.save()

    return JsonResponse({"code":1001,"msg":"发送成功"})


#测试git接口
def api_test(request):
    t = {"gitlab_url":["http://192.168.1.210:8880/root/dvwa.git","http://192.168.1.210:8880/root/test.git"]}
    return JsonResponse(t)