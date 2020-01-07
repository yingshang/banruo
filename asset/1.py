from libnmap.process import NmapProcess
import nmap
import time

nmap_proc = NmapProcess(targets='127.0.0.1', options='-sV -p 3306')
nmap_proc.run_background()




