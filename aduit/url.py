from django.urls import path

from .views import *


urlpatterns = [
    path('projects/',display_project,name='aduit_display_project'),
    path('info',project_info,name='aduit_project_info'),
    path('overview', overview,name='aduit_overview'),
    path('scan', scan,name='aduit_scan'),
    path('chandao',chandao,name='aduit_chandao'),
    path('filter_vul', filter_vul,name='aduit_filter_vul'),
    path('send_chaodao', send_chandao,name='aduit_send_chandao'),
    path('api/proj_del',api_proj_del,name='aduit_proj_del'),
    path('api/restart',restart,name='aduit_aduit_restart'),
    path('api/chandao_del',api_chandao_del,name='aduit_chandao_del'),
    path('api/list',list,name='aduit_vul_list'),
    path('api/detail',detail,name='aduit_vul_detail'),
    path('api_test', api_test),
]