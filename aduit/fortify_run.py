# coding: utf-8
import subprocess,os
from xml.dom.minidom import parse
import xml.dom.minidom
import random
import string
import pymysql
import codecs
from .models import proj_info,vul_info
from celery.decorators import task
import smtplib
from email.mime.text import MIMEText
from email.header import Header
#from celery.task.schedules import crontab
#from celery.decorators import periodic_task
import requests
import datetime
from banruo.config import *

#对fortify的XML文件进行解析
def report_xml(filename,source_path,name,token):
    DOMTree = xml.dom.minidom.parse(filename)
    Data = DOMTree.documentElement
    ReportSections3 = Data.getElementsByTagName("ReportSection")[2]
    GroupingSections = ReportSections3.getElementsByTagName("GroupingSection")
    num = 1
    for GroupingSection in GroupingSections:
        Issues = GroupingSection.getElementsByTagName("Issue")
        for i in range(len(Issues)):
            groupTitle = GroupingSection.getElementsByTagName("groupTitle")[0].childNodes[0].nodeValue  # 漏洞标题
            #count = GroupingSection.getAttribute('count')  # 漏洞号
            Folder = GroupingSection.getElementsByTagName("Folder")[0].childNodes[0].nodeValue  # 风险
            #Issue_id = Issues[i].getAttribute('iid')  # 问题ID
            Abstract = GroupingSection.getElementsByTagName("Abstract")[i].childNodes[0].nodeValue  # 问题详细
            FileName = GroupingSection.getElementsByTagName("FileName")[i].childNodes[0].nodeValue  # 文件名
            extend = FileName.split('.')[-1] #文件后缀
            FilePath = GroupingSection.getElementsByTagName("FilePath")[i].childNodes[0].nodeValue  # 文件路径
            LineStart = GroupingSection.getElementsByTagName("LineStart")[i].childNodes[0].nodeValue  # 影响行
            Snippet = GroupingSection.getElementsByTagName("Snippet")[i].childNodes[0].nodeValue  # 影响代码
            path = source_path+'/'+FilePath
            with codecs.open(path, "r", encoding='utf-8', errors='ignore') as f:
                full_code = f.read()
            vul_info.objects.update_or_create(
                                    vid = num,
                                    title = groupTitle,
                                  risk = Folder,
                                  Abstract = Abstract,
                                  FileName = FileName,
                                  FilePath = FilePath,
                                  LineStart = LineStart,
                                  Snippet = Snippet,
                                  full_code =full_code,
                                proj_id = proj_info.objects.get(token=token),
                                extend = extend,
                                  )
            num = num+1





def run(myfile,token):
    # fortify 运行的代码
    source_path = fortify_path + myfile
    fortify_fpr = report_path + myfile + '.fpr'
    fortify_xml = report_path + myfile + '.xml'
    del_fpr = 'sourceanalyzer -b ' + myfile + ' -clean'
    build = 'sourceanalyzer  -b ' + myfile + ' -Xmx1200M -Xms600M -Xss24M     -source 1.8 -machine-output   ' + source_path
    scan = 'sourceanalyzer  -b ' + myfile + ' -scan  -format fpr -f ' + fortify_fpr + ' -machine-output '
    report = 'ReportGenerator  -format xml -f ' + fortify_xml + ' -source ' + fortify_fpr + ' -template DeveloperWorkbook.xml'
    subprocess.check_call(del_fpr, shell=True)
    subprocess.check_call(build, shell=True)
    subprocess.check_call(scan, shell=True)
    subprocess.check_call(report, shell=True)
    report_xml(fortify_xml, source_path,myfile,token)
    obj = proj_info.objects.get(token=token)
    obj.total = vul_info.objects.filter(proj_id=proj_info.objects.get(token=token)).count()
    obj.status = 2
    obj.save()



@task
def git_api():
    list = []
    username = git_username.replace("@", "%40")
    if git_api_choice == 1:
        f = open(git_filepath)
        for i in f.readlines():
            if "http://" in i:
                push.delay(gitaddress=i.replace('http://', 'http://'+username+':'+git_password+'@'),type=1)
            else:
                push.delay(gitaddress=i.replace('https://', 'https://' + username + ':' + git_password + '@'),type=1)
    else:
        r = requests.get(git_api_adress)
        git_list = r.json()[parm]
#        exclude_list = ['http://test.com/1111.git', ]  # 排除的链接
        for i in git_list:
 #           if any(t == i for t in exclude_list) == False:
            if "http://" in i:
                push.delay(gitaddress=i.replace('http://', 'http://'+username+':'+git_password+'@'),type=1)
            else:
                push.delay(gitaddress=i.replace('https://', 'https://' + username + ':' + git_password + '@'),type=1)

@task
def push(gitaddress='',svnaddress='',name='',type=1,svnaccount='',svnpwd=''):
    token = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    if len(gitaddress)!=0:
        myfile = gitaddress.split('/')[-1].split('.')[0]
        proj_info.objects.create(name=myfile, git=gitaddress,token=token,type=type)
        try:
            cmd = 'git clone ' + gitaddress.strip() + ' '+ fortify_path + myfile
            print(cmd)
            subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError as err:
            try:
                subprocess.check_call('cd '+ fortify_path + myfile + ' && git pull', shell=True)
            except subprocess.CalledProcessError as err:
                pass
    elif len(name) !=0:
        myfile = name
        proj_info.objects.create(name=name, token=token, type=type)
    else:
        myfile = name
        proj_info.objects.create(name=name,token=token,type=type,svn=svnaddress)
        if len(svnaccount) ==0 and len(svnpwd) ==0:
            subprocess.check_call('svn checkout '+svnaddress+' --no-auth-cache '+fortify_path+myfile,shell=True)
        else:
            subprocess.check_call('svn checkout '+svnaddress+' --username '+svnaccount+' --password '+svnpwd+' --no-auth-cache '+fortify_path+myfile,shell=True)
    run(myfile,token)



def send_email():
    now_time = datetime.datetime.now()
    now_time = str(now_time.strftime('%Y-%m-%d'))
    sql = '''
    SELECT bb.project as project_id,bb.name,COUNT(*) as total,IFNULL(d.new,0) ,GROUP_CONCAT(bb.id)as bug_id_list from
    (SELECT a.id,c.name 
     ,a.project from zt_bug a
     LEFT JOIN zt_project c on a.project = c.id
     WHERE a.status = 'active' and a.product = '3' and a.openedDate  > '%s' )bb
    LEFT JOIN(select a.id,c.name 
     ,a.project,count(1) as new from zt_bug a
     LEFT JOIN zt_project c on a.project = c.id
     WHERE a.status = 'active' and a.product = '3' and a.openedDate  > '%s' GROUP BY a.project) as d on d.name = bb.name  
    group by bb.name
        '''%(now_time,now_time)
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DATABASE, port=MYSQL_PORT,charset="utf8")
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    td = ''
    for row in results:
        contend = ''
        try:
            chandao_id = row[4].split(',')
            for id in chandao_id:
                contend = contend + u'''<a href='http://192.168.1.210:8888/zentao/bug-view-{0}.html'>{1}  </a>
        '''.format(id, id)
        except AttributeError:
            pass
        td = td + u'''   
    <tr>
              <td style="background:#e8eaeb,text-align:center"><a href="http://192.168.1.210:8888/zentao/project-bug-%s.html">%s</a></td>
              <td style="text-align:center">%s</td>
              <td style="text-align:center">%s</td>
              <td>%s</td>
            </tr>
    ''' % (row[0], row[1], row[2], row[3],contend)
    sql = '''
    SELECT bb.product,bb.name,bb.total,IFNULL(d.new,0),GROUP_CONCAT(d.id)as bug_id_list 
    from  (select a.product,c.name,count(*) as total from zt_bug a
             LEFT JOIN zt_product c on a.product = c.id
            WHERE a.status = 'active' and a.openedBy = '1' and a.product != '3' 
            group by a.product,c.name)bb
    left join (SELECT a.id,a.product,c.name,count(1) as new from zt_bug a
           LEFT JOIN zt_product c on a.product = c.id
          WHERE a.status = 'active' and a.openedBy = '1' and a.product != '3' and a.openedDate  > '%s'
           group by   a.product,c.name
          ) as d  on d.`name` = bb.`name` and d.product = bb.product
    group by bb.name
        ''' % now_time
    cursor.execute(sql)
    results = cursor.fetchall()
    testtd = ''
    for row in results:
        contend = ''
        try:
            chandao_id = row[4].split(',')
            for id in chandao_id:
                contend = contend + u'''<a href='http://test.com/index.php?m=bug&f=view&bugID={0}'>{1}  </a>
        '''.format(id, id)
        except AttributeError:
            pass
        testtd = testtd + u'''   
    <tr>
              <td style="background:#e8eaeb,text-align:center"><a href="http://test.com/index.php?m=bug&f=browse&productID=%s">%s</a></td>
              <td style="text-align:center">%s</td>
              <td style="text-align:center">%s</td>
              <td>%s</td>
            </tr>
    ''' % (row[0], row[1], row[2],row[3], contend)
    html = u'''
    <html>
    <head>
    </head>
    <body>
    <table border="1">
    <h2>代码审计项目</h2>
    <tr>
    <th>git项目</th>
    <th>总数</th>
    <th>新增数</th>
    <th>禅道ID</th>
    </tr>
    ''' + td + u'''
    </table>
    </br>
    <h2>渗透测试项目</h2>
    <table border="1">
    <tr>
    <th>测试项目</th>
    <th>总数</th>
    <th>新增数</th>
    <th>禅道ID</th>
    </tr>
    ''' + testtd + u'''
    </table>
    </br>
    <b>注意：代码审计的结果是基于github项目进行审计，每个项目的负责人我已经在禅道上面指派了。</b></br>
    <b>还有就是漏洞误报的问题，审计的结果是正确的，但是无法进行攻击。例如：发现了一个SQL注入的漏洞，但是由于这个查询仅供内部查询调用，即黑客无法在外部找到这个漏洞</b></br>
    <b>如果发现是误报，可以直接选择关闭，当然，你也可以按照我的修复建议进行修复，加强代码质量。</b></br>
    <b>如果你已经修复的话，请告诉你在那个分支修复了，以便我重新检测。（代码审计系统默认拉取master分支）</b></br>
    <b>谢谢各位的合作！！！</b>
    </body>
    </html>
    '''
    mail_host = MAIL_HOST
    mail_user = MAIL_USER
    mail_pass = MAIL_PASSWORD
    subject = '每天禅道安全审计结果'
    sender = mail_user
    receivers = [mail_user]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    message = MIMEText(html, 'html', 'utf-8')
    message['From'] = Header("安全审计", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())



