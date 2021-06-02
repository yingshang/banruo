import subprocess, os
from xml.dom.minidom import parse
import xml.dom.minidom
import random
import string
import codecs
from .models import proj_info, vul_info
from celery.decorators import task
# from celery.task.schedules import crontab
# from celery.decorators import periodic_task
import requests
from lib.config_json import *

# 对fortify的XML文件进行解析
def report_xml(filename, source_path, name, token):

    DOMTree = xml.dom.minidom.parse(filename)
    Data = DOMTree.documentElement
    ReportSections3 = Data.getElementsByTagName("ReportSection")[2]
    GroupingSections = ReportSections3.getElementsByTagName("GroupingSection")
    num = 1
    for GroupingSection in GroupingSections:
        Issues = GroupingSection.getElementsByTagName("Issue")
        for i in range(len(Issues)):
            groupTitle = GroupingSection.getElementsByTagName("groupTitle")[0].childNodes[0].nodeValue  # 漏洞标题
            # count = GroupingSection.getAttribute('count')  # 漏洞号
            Folder = GroupingSection.getElementsByTagName("Folder")[0].childNodes[0].nodeValue  # 风险
            # Issue_id = Issues[i].getAttribute('iid')  # 问题ID
            Abstract = GroupingSection.getElementsByTagName("Abstract")[i].childNodes[0].nodeValue  # 问题详细
            FileName = GroupingSection.getElementsByTagName("FileName")[i].childNodes[0].nodeValue  # 文件名
            extend = FileName.split('.')[-1]  # 文件后缀
            FilePath = GroupingSection.getElementsByTagName("FilePath")[i].childNodes[0].nodeValue  # 文件路径
            LineStart = GroupingSection.getElementsByTagName("LineStart")[i].childNodes[0].nodeValue  # 影响行
            Snippet = GroupingSection.getElementsByTagName("Snippet")[i].childNodes[0].nodeValue  # 影响代码

            path = source_path + '/' + FilePath

            try:
                f = open(path,"r",encoding='utf8')
                full_code  = f.read()
                f.close()
            except FileNotFoundError:
                full_code = "文件可能不在这一层目录，可能在上一层"

            vul_info.objects.update_or_create(
                vid=num,
                title=groupTitle,
                risk=Folder,
                Abstract=Abstract,
                FileName=FileName,
                FilePath=FilePath,
                LineStart=LineStart,
                Snippet=Snippet,
                full_code=full_code,
                proj_id=proj_info.objects.get(token=token),
                extend=extend,
            )
            num = num + 1


def run(myfile, token):
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
    report_xml(fortify_xml, source_path, myfile, token)
    obj = proj_info.objects.get(token=token)
    obj.total = vul_info.objects.filter(proj_id=proj_info.objects.get(token=token)).count()
    obj.status = 2
    obj.save()


@task
def git_api():
    list = []
    username = GIT_USERNAME.replace("@", "%40")
    if GIT_API_CHOICE == 1:
        f = open(GIT_PATH)
        for i in f.readlines():
            if "http://" in i:
                push.delay(gitaddress=i.replace('http://', 'http://' + username + ':' + GIT_PASSWORD + '@'), type=1)
            else:
                push.delay(gitaddress=i.replace('https://', 'https://' + username + ':' + GIT_PASSWORD + '@'), type=1)
    else:
        r = requests.get(GIT_ADDRESS)
        git_list = r.json()[GIT_PARM]
        #        exclude_list = ['http://test.com/1111.git', ]  # 排除的链接
        for i in git_list:
            #           if any(t == i for t in exclude_list) == False:
            if "http://" in i:
                push.delay(gitaddress=i.replace('http://', 'http://' + username + ':' + GIT_PASSWORD + '@'), type=1)
            else:
                push.delay(gitaddress=i.replace('https://', 'https://' + username + ':' + GIT_PASSWORD + '@'), type=1)


@task
def push(gitaddress='', svnaddress='', name='', type=1, svnaccount='', svnpwd=''):
    token = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    if len(gitaddress) > 0:
        myfile = gitaddress.split('/')[-1].split('.')[0]
        proj_info.objects.create(name=myfile, git=gitaddress, token=token, type=type)
        try:
            cmd = 'git clone ' + gitaddress.strip() + ' ' + fortify_path + myfile
            subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError as err:
            try:
                subprocess.check_call('cd ' + fortify_path + myfile + ' && git pull', shell=True)
            except subprocess.CalledProcessError as err:
                pass
    elif len(name) > 0:
        myfile = name
        proj_info.objects.create(name=name, token=token, type=type)
    elif len(svnaddress)>0:
        myfile = svnaddress.split("/")[-1]

        proj_info.objects.create(name=myfile, token=token, type=type, svn=svnaddress)
        try:
            if len(svnaccount) == 0 and len(svnpwd) == 0:
                subprocess.check_call('svn checkout ' + svnaddress + ' --no-auth-cache ' + fortify_path + myfile,
                                      shell=True)
            else:
                subprocess.check_call(
                    'svn checkout ' + svnaddress + ' --username ' + svnaccount + ' --password ' + svnpwd + ' --no-auth-cache ' + fortify_path + myfile,
                    shell=True)
        except subprocess.CalledProcessError:
            pass
    run(myfile, token)
