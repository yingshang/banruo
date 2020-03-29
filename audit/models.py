from django.db import models
import datetime



class proj_info(models.Model):
    name = models.CharField(max_length=100)    #项目名字
    git = models.CharField(max_length=100,null=True,blank=True)      #git地址
    total = models.CharField(max_length=10,default='0',null=True) #该项目漏洞总数
    token = models.CharField(max_length=100,null=True,blank=True)#项目标识
    status = models.IntegerField(default=1)#确定扫描是否完成
    type = models.IntegerField(blank=True,null=True)#项目类型，1为git，2为svn，3为上传
    svn = models.CharField(max_length=100,blank=True,null=True)#svn
    time = models.DateTimeField(auto_now=True) #扫描时间

    class Meta:
        permissions  = (
            ("upload_code_and_scan","可以上传代码并且进行代码审计扫描"),
            ("restart_scan","重新进行代码审计扫描"),
            ("display_projects","展示所有代码审计项目"),
            ("display_info","展示一个项目的详细信息"),
            ("delelte_project","删除代码审计项目"),
        )




class vul_info(models.Model):
    vid = models.IntegerField()        #用来辨别每个页面的id
    title = models.CharField(max_length=200)       #漏洞名称
    risk = models.CharField(max_length=10)        #漏洞风险
    Abstract = models.TextField()                 #漏洞原因
    FileName = models.CharField(max_length=50)      #文件名
    FilePath = models.CharField(max_length=200)     #文件位置
    LineStart = models.CharField(max_length=10)     #影响行
    Snippet = models.TextField()         #影响行的代码
    full_code = models.TextField()         #全部的代码
    extend = models.CharField(max_length=50)     #后缀名
    proj_id = models.ForeignKey(proj_info,on_delete=models.CASCADE)      #项目标识
    time = models.DateTimeField(auto_now=True)     #扫描时间
    class Meta:
        permissions  = (
            ("vullist","返回一个项目的漏洞列表"),
            ("vuldetail","返回一个项目的漏洞列表具体信息"),
        )


class chandao_data(models.Model):
    proj_name = models.CharField(max_length=100,default='') #项目名字
    vul_name = models.CharField(max_length=200)
    md5  = models.CharField(max_length=100)
    Abstract = models.TextField()  # 漏洞原因
    FileName = models.CharField(max_length=50)  # 文件名
    FilePath = models.CharField(max_length=200)  # 文件位置
    LineStart = models.CharField(max_length=10)  # 影响行
    describe = models.TextField() #漏洞描述
    Recommendation = models.TextField() #漏洞修复方式
    hidden = models.IntegerField(default=0) #用于删除之后不会在发送到禅道里面
    status = models.IntegerField(default=0)#状态0为未发送到禅道，1则为发送到禅道

    class Meta:
        permissions = (
            ("chandao_index", "展示禅道主页"),
            ("hidden_vul", "隐藏发送到禅道的漏洞"),
            ("filter_vul", "过滤发送到禅道的漏洞"),
            ("send_vul", "发送到禅道的漏洞"),
        )

class chandao_person_info(models.Model):
    header = models.CharField(max_length=10)
    ename = models.CharField(max_length=100)
    cname = models.CharField(max_length=200)
    pid = models.CharField(max_length=10)



