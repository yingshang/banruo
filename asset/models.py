from django.db import models

# Create your models here.

#扫描任务
class scantask(models.Model):
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    masscan_status = models.CharField(max_length=100) #扫描状态
    scantime = models.DateTimeField() #扫描时间
    endtime = models.DateTimeField(null=True)#结束时间



#扫描IP地址
class scanIP(models.Model):
    ip = models.CharField(max_length=100)
    name = models.CharField(max_length=100,blank=True,null=True)
    scantime = models.DateTimeField()  # 扫描时间
    rate = models.CharField(max_length=100,default='0.00') #扫描进度
    endtime = models.DateTimeField(null=True)#结束时间
    task = models.ForeignKey(scantask,on_delete=models.CASCADE)

#IP端口情况
class scan_ip_info(models.Model):
    port = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    cpe = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    ipfor = models.ForeignKey(scanIP,on_delete=models.CASCADE)



#nmap扫描进度
# class nmapscan(models.Model):
#     ip = models.CharField(max_length=100)
#     scantime = models.DateTimeField(auto_now=True)  # 扫描时间
#     rate = models.CharField(max_length=100,default='0.00') #扫描进度
#     endtime = models.DateTimeField(null=True)#结束时间
#     task = models.ForeignKey(scantask,on_delete=models.CASCADE)



#保存扫描资产列表
class scanlist(models.Model):
    ips = models.CharField(max_length=100)
