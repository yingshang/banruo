#celery -A tasks worker --loglevel=info --concurrency=10
#app = Celery('tasks', broker='redis://localhost:6379/0')

import nmap
from libnmap.process import NmapProcess
from asset.models import *
import masscan
from celery.decorators import task
from IPy import IP
import re
from django.utils import timezone
import random
import string
import time


@task
def nmap_scan(ip,ports,taskid):
    nmapscan.objects.create(ip=ip,task_id=taskid)
    result = nmapscan.objects.get(task_id=taskid)
    nmap_proc = NmapProcess(targets=ip, options='-sV -p  '+ports)
    nmap_proc.run_background()

    while nmap_proc.is_running():
        result.rate = str(nmap_proc.progress)
        result.save()
        time.sleep(2)  # 两秒更新一次百分比
    result.endtime = timezone.now()
    result.save()

    nm = nmap.PortScanner()

    print(nm.analyse_nmap_xml_scan(nmap_proc.stdout))

    # nm = nmap.PortScanner()
    # nm.scan(hosts=ip, ports=ports,arguments='-sV')
    # scanIP.objects.get_or_create(ip=ip)
    # scan_ip_info.objects.filter(ipfor_id=scanIP.objects.get(ip=ip).id).delete()
    #
    # for port,v in nm[ip]['tcp'].items():
    #     scan_ip_info.objects.get_or_create(port=port,name=v['name'],state=v['state'],product=v['product']+'  '+v['version'],cpe=v['cpe'],ipfor_id=scanIP.objects.get(ip=ip).id)



@task
def masscan_scan(ip):
    mas = masscan.PortScanner()
    name = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    scantask.objects.create(name=name,ip = ip,status='扫描中')
    result = scantask.objects.get(name=name)
    try:
        mas.scan(ip, ports='1-65535', arguments='--max-rate 100000')
        for ip,values in mas.scan_result['scan'].items():
            ports = ''
            for port,_ in values['tcp'].items():
                ports = ports+str(port)+','

            nmap_scan.delay(ip,ports,result.id)

        result.status = "完成扫描"
        result.endtime = timezone.now()
        result.save()
    except masscan.masscan.NetworkConnectionError:
        result.status = "网络不可用"
        result.save()

#解析IP格式是否正确
def parse_ip(ips):
    if '-' in ips:
        ipx = ips.split('-')

        ip2num = lambda x: sum([256 ** i * int(j) for i, j in enumerate(x.split('.')[::-1])])
        num2ip = lambda x: '.'.join([str(x // (256 ** i) % 256) for i in range(3, -1, -1)])
        a = [num2ip(i) for i in range(ip2num(ipx[0]), ip2num(ipx[1]) + 1) if not ((i + 1) % 256 == 0 or (i) % 256 == 0)]
        if len(a)==0:
            return False
        else:
            return True
    elif '/' in ips:
        try:
            status = IP(ips)
            return True
        except:
            return False
    else:
        compile_ip = re.compile(
            '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        if compile_ip.match(ips):
            return True
        else:
            return False

#扫描任务/进度
def scan_task():
    pass







#def masscan_scan(ip):
    # filename = ip.replace('/','_')
    # path = '/opt/'
    # subprocess.check_call('masscan -p 1-65535 --wait 2 --range %s  -oJ %s%s.json --rate 100000' %(ip,path,filename),shell=True)
    # f = open(path+filename+'.json')
    # f = open('c:\\scan.json',encoding='utf-8')
    # records = f.readlines()
    # f.close()

    # for record in records:
    #     print(record.replace(',\n',''))
    #     rs = eval(record.replace(',\n',''))
    #     print(rs)
    #     print(type(rs))
    #     results.append({rs['ip']:rs['ports'][0]['port']})

    # merged = {}
    # for d in results:
    #     for k, v in d.items ():
    #         if k not in merged:
    #             merged [k] = []
    #         merged [k].append (v)
    # for ip,port in merged.items():
    #
    #     ports = ','.join('%s' %i for i in port)
    #     print(ip)
    #     print(ports)
    #     nmap_scan(ip,ports)




