from django.shortcuts import render
from django.http import  JsonResponse
from .models import *
from .port_scan import *
from django.views.decorators.csrf import csrf_exempt
import time


def asset_info(request):
    return render(request,'asset/assetinfo.html',locals())

def ip_info(request):
    ip = request.GET.get('ip')
    return render(request,'asset/ipinfo.html',locals())

def asset_info_api(request):
    ip = request.GET.get('ip')
    try:
        page = int(request.GET.get("page")) or 1
    except:
        page = 1
    try:
        limit = int(request.GET.get("limit")) or 30
    except:
        limit = 30
    start = (page - 1) * limit
    end = page * limit
    datas = []
    if ip == None:
        rs = scanIP.objects.all()[start:end]
        for r in rs:
            datas.append({'id':r.id,'ip':r.ip,'opennum':scan_ip_info.objects.filter(ipfor_id=r.id).count(),'vulnum':1})
        count = scanIP.objects.all().count()

    else:
        rs = scanIP.objects.filter(ip=ip)
    return JsonResponse({"code": 0, "msg": "", "count": count, "data": datas}, safe=False)



def ip_info_api(request):
    ip = request.GET.get("ip")
    id = scanIP.objects.get(ip=ip)
    data = []
    rs = scan_ip_info.objects.filter(ipfor_id=id).values("port","name","product","cpe","state")
    for r in rs:
        data.append(r)

    count = scan_ip_info.objects.filter(ipfor_id=id).count()

    return JsonResponse({"code": 0, "msg": "", "count": count, "data": data}, safe=False)

@csrf_exempt
def asset_scan(request):
    if request.method == 'POST':
        ips = request.POST.get('ips')
        #清空扫描列表
        scanlist.objects.all().delete()
        #分割扫描列表
        for ip in ips.split('\n'):
            if len(ip)>0:
                if parse_ip(ip) ==True:

                    scanlist.objects.create(ips=ip)
                else:
                    return JsonResponse({'code':0,'msg':'提交的IP错误，请重新输入！！！'})
        return JsonResponse({'code':1,'msg':'提交成功'})
    rs = scanlist.objects.all()
    results = ""
    for i in rs:
        results = results + i.ips + '\n'

    return render(request,'asset/scan.html',locals())

def asset_scan_api(request):
    count = scanlist.objects.all().count()
    if count ==0 :
        return JsonResponse({'code':0,'msg':'请输入资产IP地址进行扫描'})
    else:
        rs = scanlist.objects.all()
        for r in rs:
            masscan_scan.delay(r.ips)
        return JsonResponse({'code':1,'msg':'扫描现在开始！！请稍等'})

def get_scan_task(request):
    rs = scantask.objects.all()
    count = scantask.objects.all().count()
    data = []
    if count > 0:
        for i in rs.values('id',"name","ip","masscan_status","scantime","endtime"):
            i['scantime'] = i['scantime'].strftime('%Y-%m-%d %H:%M:%S')
            try:
                i['endtime'] = i['endtime'].strftime('%Y-%m-%d %H:%M:%S')
            except AttributeError:
                pass


            nmaprs = scanIP.objects.filter(task_id=i['id'])
            nmapcount =  nmaprs.count()
            #计算nmap的总体扫描进度
            cs = 0
            for nr in nmaprs:
                cs = cs+float(nr.rate)
            #nmap扫描进度
            try:
                ns = cs/nmapcount
            except ZeroDivisionError:
                ns = 0

            i['ns'] = str(round(float(ns),2))+'%'
            data.append(i)



    return JsonResponse({"code": 0, "msg": "", "count": count, "data": data}, safe=False)


def check_nmap(request):
    id = request.GET.get("id")
    rs = scanIP.objects.filter(task_id=id)

    return render(request,'asset/nmap.html',locals())
