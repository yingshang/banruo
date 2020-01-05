#celery -A tasks worker --loglevel=info --concurrency=10

import nmap
import subprocess
from asset.models import *

#app = Celery('tasks', broker='redis://localhost:6379/0')

#@app.task
def nmap_scan(ip,ports):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip, ports=ports,arguments='-sV')
    scanIP.objects.get_or_create(ip=ip)
    scan_ip_info.objects.filter(ipfor_id=scanIP.objects.get(ip=ip).id).delete()
    for port,v in nm[ip]['tcp'].items():
        scan_ip_info.objects.get_or_create(port=port,name=v['name'],product=v['product']+'  '+v['version'],cpe=v['cpe'],ipfor_id=scanIP.objects.get(ip=ip).id)




def masscan_scan(ip):
    filename = ip.replace('/','_')
    subprocess.check_call('masscan -p 1-65535 --wait 2 --range %s  -oJ %s.json --rate 100000' %(ip,filename),shell=True)
    f = open(filename+'.json')
    records = f.readlines()
    f.close()

    results = []
    for record in records:
        try:
            rs = eval(record.replace(',\n',''))
            results.append({rs['ip']:rs['ports'][0]['port']})
        except NameError:
            pass
    merged = {}
    for d in results:
        for k, v in d.items ():
            if k not in merged:
                merged [k] = []
            merged [k].append (v)
    for ip,port in merged.items():

        ports = ','.join('%s' %i for i in port)
        nmap_scan(ip,ports)

