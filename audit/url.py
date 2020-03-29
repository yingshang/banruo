from django.urls import path

from .views import *


urlpatterns = [
    path('projects/',display_project,name='audit_display_project'),
    path('info',project_info,name='audit_project_info'),
    path('scan', scan,name='audit_scan'),
    path('chandao',chandao,name='audit_chandao'),
    path('filter_vul', filter_vul,name='audit_filter_vul'),
    path('send_chaodao', send_chandao,name='audit_send_chandao'),
    path('api/proj_del',api_proj_del,name='audit_proj_del'),
    path('api/restart',restart,name='audit_audit_restart'),
    path('api/chandao_hidden',api_chandao_hidden,name='audit_chandao_hidden'),
    path('api/vullist',vullist,name='audit_vul_list'),
    path('api/vuldetail',vuldetail,name='audit_vul_detail'),

]