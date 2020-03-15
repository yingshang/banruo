from django.urls import path
from .views import *

urlpatterns = [
    path('asset_info', asset_info, name='asset_info'),
    path('ip_info', ip_info, name='ip_info'),
    path('asset_info_api', asset_info_api, name='asset_info_api'),
    path('ip_info_api', ip_info_api, name='ip_info_api'),
    path('asset_scan', asset_scan, name='asset_scan'),
    path('asset_scan_api', asset_scan_api, name='asset_scan_api'),
    path('get_scan_task', get_scan_task, name='get_scan_task'),
    path('check_nmap', check_nmap, name='check_nmap'),



]
