from django.urls import path

from .views import *


urlpatterns = [
    path('overview/',overview,name='index_overview'),
    path('',base,name='index_base'),
    path('login/',login,name='index_login'),
    path('logout/',logout,name='index_logout'),
    #path('index/',index,name='index_index'),

]

handler403 = permission_denied
