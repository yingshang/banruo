from django.shortcuts import render,HttpResponseRedirect
import time, datetime
from audit.models import *
from django.db.models import Q
import calendar
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate


# Create your views here.

def overview(request):
    t = request.GET.get("t")
    if t == "week":
        dates = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        totals = []
        Week = datetime.datetime.now().isoweekday()
        time1 = datetime.date.today() - datetime.timedelta(days=Week - 1)
        time2 = time1 + datetime.timedelta(days=6)
        for i in range(Week):
            day = datetime.date.today() - datetime.timedelta(days=Week - 2 - i)
            day1 = datetime.date.today() - datetime.timedelta(days=Week - i - 1)
            obj = proj_info.objects.filter(time__range=(day1, day))
            if obj:
                total = 0
                for i in obj:
                    total = total + int(i.total)
                totals.append(total)
            else:
                totals.append(0)
        critical_title = vul_info.objects.filter(time__range=(time1, time2)).filter(
            Q(risk='Critical') | Q(risk='High')).values('title').annotate(Count('title'))

    elif t == "month":
        dates = []
        now = datetime.date.today()
        year = now.year
        month = now.month
        totals = []
        day = calendar.monthrange(2018, 5)[1]
        for i in range(1, day):
            dates.append(i)
            try:
                obj = proj_info.objects.filter(time__range=(
                str(year) + "-" + str(month) + "-" + str(i), str(year) + "-" + str(month) + "-" + str(i + 1)))
            except:
                t1 = str(year) + "-" + str(month) + "-" + str(i)
                t2 = str(year) + "-" + str(month + 1) + "-1"
                obj = proj_info.objects.filter(time__range=(t1
                                                            , t2))
            if obj:
                total = 0
                for i in obj:
                    total = total + int(i.total)
                totals.append(total)
            else:
                totals.append(0)

        time1 = datetime.datetime.fromtimestamp(
            time.mktime(time.strptime(str(year) + '-' + str(month) + '-1', "%Y-%m-%d")))
        time2 = datetime.datetime.fromtimestamp(
            time.mktime(time.strptime(str(year) + '-' + str(month) + '-' + str(day - 1), "%Y-%m-%d")))
        critical_title = vul_info.objects.filter(time__range=(time1, time2)).filter(
            Q(risk='Critical') | Q(risk='High')).values('title').annotate(Count('title'))
    elif t == "year":
        dates = []
        now = datetime.date.today()
        year = now.year
        month = now.month
        totals = []
        for i in range(1, 13):
            dates.append(str(i) + "月")
            try:
                obj = proj_info.objects.filter(
                    time__range=(str(year) + "-" + str(i) + "-1", str(year) + "-" + str(i + 1) + "-1"))
            except:
                obj = proj_info.objects.filter(time__range=(str(year) + "-" + str(i) + "-1", str(year + 1) + "-1-1"))
            if obj:
                total = 0
                for i in obj:
                    total = total + int(i.total)
                totals.append(total)
            else:
                totals.append(0)
        time1 = datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(year) + '-1-1', "%Y-%m-%d")))
        time2 = datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(year) + '-12-30', "%Y-%m-%d")))
        critical_title = vul_info.objects.filter(time__range=(time1, time2)).filter(
            Q(risk='Critical') | Q(risk='High')).values('title').annotate(Count('title'))
    else:
        dates = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        totals = []
        Week = datetime.datetime.now().isoweekday()
        time1 = datetime.date.today() - datetime.timedelta(days=Week - 1)
        time2 = time1 + datetime.timedelta(days=6)
        for i in range(Week):
            day = datetime.date.today() - datetime.timedelta(days=Week - 2 - i)
            day1 = datetime.date.today() - datetime.timedelta(days=Week - i - 1)
            obj = proj_info.objects.filter(time__range=(day1, day))
            if obj:
                total = 0
                for i in obj:
                    total = total + int(i.total)
                totals.append(total)
            else:
                totals.append(0)
        critical_title = vul_info.objects.filter(time__range=(time1, time2)).filter(
            Q(risk='Critical') | Q(risk='High')).values('title').annotate(Count('title'))
    return render(request, "index/overview.html", locals())

@login_required()
def base(request):
    user = request.user
    return render(request, "index/base.html", locals())


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            err_msg = "账号或者密码错误"
            return render(request, 'index/login.html', locals())


    else:
        return render(request,'index/login.html',locals())


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


def permission_denied(request):
    return render(request, 'index/403.html')