from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.http.response import HttpResponse
from .models import *
import time, datetime
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.db.models import Q
from .fortify_run import push, git_api
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from .info import information
import hashlib
import pymysql
from celery.decorators import task
from lib.config_json import *


@permission_required("audit.display_projects")
def display_project(request):
    keyword = request.GET.get("keyword")
    try:
        page = int(request.GET.get("page")) or 1
    except:
        page = 1
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
    return render(request, "audit/projects.html", locals())


@permission_required("audit.display_info")
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
    critical_title = vul_info.objects.filter(proj_id=id).filter(Q(risk='Critical') | Q(risk='High')).values(
        'title').annotate(Count('title'))  # 严重和高危漏洞标题
    # vul_title = vul_info.objects.filter(proj_id=id).values('title').annotate(Count('title'))  # 所有漏洞标题
    return render(request, "audit/info.html", locals())


@permission_required("audit.vullist")
@csrf_exempt
def vullist(request):
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
                'line_number': vul.LineStart,
                'file_path': vul.FilePath,
                'level': vul.risk,
                'rule_name': vul.title,
                'language': vul.extend,
                'describe': information(vul.title)['describe'],
                'Recommendation': information(vul.title)['Recommendation'],
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
            }}, safe=False)
    else:
        return HttpResponse('must be post method ')

@permission_required("audit.vuldetail")
@csrf_exempt
def vuldetail(request):

    id = request.POST.get('id')
    vid = request.POST.get('vid')
    code = vul_info.objects.filter(proj_id=id).get(vid=vid).full_code
    extend = vul_info.objects.filter(proj_id=id).get(vid=vid).extend
    return JsonResponse({
        'code': 1001,
        'result': {
            'file_content': code,
            'extension': extend,
        }
    })

@permission_required("audit.delelte_project")
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

@permission_required("audit.hidden_vul")
@csrf_exempt
def api_chandao_hidden(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids')
        for id in ids:
            try:
                obj = chandao_data.objects.get(id=id)
                obj.hidden = 1
                obj.save()
            except:
                return JsonResponse({
                    "code": 1002,
                    "msg": "传入内容错误"
                })
        return JsonResponse({
            'code': 1001,
            'msg': '隐藏成功'
        })
    else:
        return JsonResponse({
            'code': 1000,
            'msg': '必须使用POST方式'
        })

@csrf_exempt
@permission_required('audit.upload_code_and_scan')
def scan(request):
    if request.method == 'POST':
        t = request.POST.get('type')  # 1为git,2为git-list,3为SVN,4为上传
        if (t == "1"):
            gitaddress = request.POST.get("git_address")
            gitaccount = request.POST.get("git_username")
            gitpwd = request.POST.get("git_password")

            if len(gitaccount) == 0 and len(gitpwd) == 0:
                push.delay(gitaddress=gitaddress)
                return JsonResponse({"code": 1001, "msg": "开始扫描"})
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
        elif (t == "2"):
            git_api()
            return JsonResponse({"code": 1001, "msg": "开始扫描!!!"})
        elif (t == "3"):
            svnaddress = request.POST.get("svn_address")
            svnaccount = request.POST.get("svn_username")
            svnpwd = request.POST.get("svn_password")
            push.delay(svnaddress=svnaddress, type=3, svnaccount=svnaccount, svnpwd=svnpwd)
            return JsonResponse({"status": 0, "msg": "开始扫描!!!"})
        elif (t == "4"):
            myFile = request.FILES.get("file", None)
            name = myFile.name
            if not myFile:
                return JsonResponse({"status": 0, "msg": "上传失败!!!"})
            elif myFile.name.split('.')[-1] != 'zip':
                return JsonResponse({"status": 2, "msg": "上传文件必须为ZIP!!!"})
            else:
                destination = open(os.path.join("/data/fortify/", myFile.name), 'wb+')
                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()
                os.system("unzip -o  /data/fortify/" + myFile.name + "  -d  /data/fortify/" + name.split('.')[0])
                push.delay(name=name.split('.')[0], type=4)
                return JsonResponse({"status": 1, "msg": "上传成功!!!"})

        else:
            return JsonResponse({"status": 0, "msg": "参数类型错误"})

    else:
        address = GIT_ADDRESS
        p = GIT_PARM
        choice = GIT_API_CHOICE
        filepath = GIT_PATH
        return render(request, "audit/scan.html", locals())


@permission_required("audit.restart_scan")
@csrf_exempt
def restart(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            type = proj_info.objects.get(id=id).type
            if type == 1:
                git = proj_info.objects.get(id=id).git
                push.delay(gitaddress=git)

            elif type == 3:
                svn = proj_info.objects.get(id=id).svn
                push.delay(svnaddress=svn)
            elif type == 4:
                return JsonResponse({"code": 8888, "msg": "该项目是压缩上传，请重新上传压缩文件进行扫描"})
            else:
                return JsonResponse({"code": 9999, "msg": "项目类型未知，无法重新扫描。"})

        except:
            return JsonResponse({"code": 1000, "msg": "内容错误！！！"})
        return JsonResponse({"code": 1001, "msg": "开始扫描!!!"})
    else:
        return JsonResponse({"code": 1111, "msg": "请求方式必须为POST!!!"})


@permission_required("audit.chandao_index")
def chandao(request):
    keyword = request.GET.get("keyword")
    try:
        page = int(request.GET.get("page")) or 1
    except:
        page = 1
    try:
        limit = int(request.GET.get("limit")) or 10
    except:
        limit = 10

    start = (page - 1) * limit
    end = page * limit
    if keyword == None:
        results = chandao_data.objects.all().exclude(hidden=1)[start:end]
        vul_count = chandao_data.objects.all().exclude(hidden=1).count()

    else:
        results = chandao_data.objects.filter(vul_name__icontains=keyword).exclude(hidden=1)[start:end]
        vul_count = chandao_data.objects.filter(vul_name__icontains=keyword).exclude(hidden=1).count()

    return render(request, "audit/chandao.html", locals())

@permission_required("audit.filter_vul")
def filter_vul(request):
    results = vul_info.objects.all()
    for i in results:
        # if i.risk =='Critical':
        # if any(t  in i.title for t in filter_title):
        m = i.title.replace('\n', '') + i.FileName.replace('\n', '') + i.LineStart.replace('\n',
                                                                                           '') + i.FilePath.replace(
            '\n', '')  # md5的明文
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
                vul_name=vul_name,
                FilePath=FilePath,
                Abstract=Abstract,
                FileName=FileName,
                describe=describe,
                Recommendation=Recommendation,
                LineStart=LineStart,
                proj_name=proj_name,
            )
    return JsonResponse({"code": 1001, "msg": "过滤漏洞成功"})


@permission_required("audit.send_vul")
def send_chandao(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    results = chandao_data.objects.all()
    for i in results:
        if i.status == 0:
            if i.hidden == 0:
                cinfo = chandao_person_info.objects.get(ename=i.proj_name)
                title = i.proj_name.strip() + '_' + i.vul_name.strip()

                # describe = cgi.escape(i.describe)
                # Recommendation = cgi.escape(i.Recommendation)
                project_id = cinfo.pid
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
                ''' % (i.md5, i.Abstract, i.FileName, i.FilePath, i.LineStart, i.describe, i.Recommendation)
                conn = pymysql.connect(host=CHANDAO_MYSQL_HOST, user=CHANDAO_MYSQL_USER, passwd=CHANDAO_MYSQL_PASSWORD, db=CHANDAO_MYSQL_DATABASE,
                                       port=int(CHANDAO_MYSQL_PORT), charset="utf8")
                cursor = conn.cursor()
                sql = "SELECT * from zt_user where realname = '%s'" % header
                cursor.execute(sql)
                try:
                    header = cursor.fetchall()[0][2]
                except IndexError:
                    pass
                sql = "select id from zt_project where name='%s'" % i.proj_name
                cursor.execute(sql)
                # module =cursor.fetchall()[0][0]

                # 插入禅道bug
                sql = "INSERT INTO `zt_bug` SET `product` = % s,`module` = 0,`hardware` = '1',`lastEditedDate` = '2019-12-03 20:21:36'," \
                      "`linkBug` = '1',`resolvedDate` = '2019-12-03 20:21:36',`deadline` = '2019-12-03 20:21:36',`activatedDate` = '2019-12-03 20:21:36',`activatedCount` = '0',`closedDate` = '2019-12-03 20:21:36'," \
                      "`duplicateBug` = '0',`project` = % s,`openedBuild` = 'trunk',`assignedTo` = % s,`mailto` = '',`type` = 'security'," \
                      "`os` = '',`browser` = '',`color` = '',`title` = % s,`severity` = '4',`pri` = '4',`steps` = % s,`story` = '0',`task` = '0'," \
                      "`keywords` = '',`case` = '0',`caseVersion` = '0',`result` = '0',`testtask` = '0',`openedBy` = % s,`openedDate` = % s," \
                      "`assignedDate` = % s;"
                cursor.execute(sql, (
                str(PRODUCT_ID), str(project_id), header, title, contend, OPENEDBY, openedDate, assignedDate))
                bug_id = int(conn.insert_id())  # 最新插入行的主键ID
                conn.commit()
                # 关联bug表的更新
                sql2 = "INSERT INTO `zt_action` SET `objectType` = 'security',`objectID` = %s,`actor` = %s,`action` = 'opened'," \
                       "`date` = '2019-12-03 20:21:36',`comment` = '',`extra` = '',`product` = ',1,',`project` = %s" % (
                           bug_id, OPENEDBY, project_id)
                cursor.execute(sql2)
                conn.commit()
                cursor.close()
                i.status = 1
                i.save()


    return JsonResponse({"code": 1001, "msg": "发送成功"})

