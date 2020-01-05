from django.db import models

# Create your models here.

#扫描IP地址
class scanIP(models.Model):
    ip = models.CharField(max_length=100)
    name = models.CharField(max_length=100,blank=True,null=True)

class scan_ip_info(models.Model):
    port = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    cpe = models.CharField(max_length=200)
    ipfor = models.ForeignKey(scanIP,on_delete=models.CASCADE)

#保存扫描资产列表
class scanlist(models.Model):
    ips = models.CharField(max_length=100)
