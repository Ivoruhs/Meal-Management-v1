import calendar
from calendar import monthrange
import datetime
from distutils.log import Log
# from typing import re

from django.conf import settings
from django.conf.global_settings import LOGIN_REDIRECT_URL
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count
from django.http.response import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from meal.models import Employee, Log
from prochito.forms import LogForm, multilogForm







@login_required(login_url='signin')
# @user_passes_test(lambda u: u.is_superuser)
# @user_passes_test(lambda u: u.groups.filter(name='meal-manager').count() == 0, login_url='/meal/signin/')
def home(request):
        month=['January','February','March','April','May','June','Juny','August','September','October','November','December']
        is_manager = request.user.groups.filter(name='meal-manager').exists()
        if is_manager==False:
            current_user = request.user.id
            eid=Employee.objects.filter(user_id=current_user).values('id')
            eid=eid[0]['id']
            return HttpResponseRedirect(reverse('multiadd',args=(eid,)))


        all = Employee.objects.all()
        date = datetime.date.today()

        if request.GET.get('month'):
            m=request.GET.get('month')
            m=int(m)
            date=date.replace(month=m)

        cm=date.month
        base = datetime.datetime(date.year, date.month, 1)
        days = monthrange(datetime.datetime.now().year, date.month)[1]

        date_list = [(base + datetime.timedelta(days=x)).date() for x in range(0, days)] #contains a list of all days in the selected month

        c = Log.objects.filter(date=datetime.datetime.now().date()).count()
        now = datetime.datetime.now()

        #count employee's total log
        emps = Employee.objects.all()
        monthly_entry_count = dict()
        for i in emps:
            cnt=len(Log.objects.filter(eid=i.id,date__month=cm))
            monthly_entry_count[i.id]=cnt


        # print(monthly_entry_count)


        date=Log.objects.filter(date__month=datetime.datetime.now().month, date__year=datetime.datetime.now().year).values('date','eid').distinct()
        context={"employees":all, "count":c,"date_list":date_list,"month":month,"current_month":cm,"monthly_entry_count":monthly_entry_count}
        return render(request,'meal/home.html',context=context)







@csrf_exempt
def add(request):
    # print('inside add')

    if request.method=='POST':

        f=LogForm(request.POST)


        if f.is_valid():
            # print('inside f valid')
            l=f.save(commit=True)
            c=Log.objects.filter(date=datetime.datetime.now().date()).count()
            return HttpResponse(c)


        else:
            return HttpResponse(f.errors)
    else:
        f=LogForm()
    return HttpResponse('ok')

#for testing
# @csrf_exempt
# def add(request):
#     if request.method=='POST':
#         f=LogForm(request.POST)
#         if f.is_valid():
#             f.save(commit=True)
#             print('f valid')
#             return HttpResponse('form valid response')
#         else:
#             return HttpResponse('form not valid resposne')
#     return HttpResponse('default response')



@csrf_exempt
def delete(request):
    if request.method=='POST':
        f=LogForm(request.POST)
        if f.is_valid():
            eid=request.POST['eid']
            date=request.POST['date']
            d=Log.objects.filter(date=date,eid=eid)
            d.delete()
            c=Log.objects.filter(date=datetime.datetime.now().date()).count()
            return HttpResponse(c)


        else:
            return HttpResponse("Date or time has passed. Can't modify now!")
            # return HttpResponse(f.errolds=['date']
    def clean_date(self):
        date = self.cleaned_data['date']
        # print(date)rs)

    return HttpResponse("default")


@login_required(login_url='signin')
def multiadd(request,id):
      if request.method=='POST':

            # return HttpResponse(datetime.datetime.now().time().hour)

            f=multilogForm(request.POST)
            if f.is_valid():
                m=f.save(commit=False)
                m.eid=Employee.objects.get(pk=id)
                m.save()
                is_manager = request.user.groups.filter(name='meal-manager').exists()
                if is_manager==True:
                    return redirect('home')
                else:
                    # return HttpResponse("Successful")
                    return HttpResponseRedirect(reverse('multiadd',args=(id,)))

      else:
        f=multilogForm()

      l=Log.objects.filter(eid=id).order_by('date')
      month=[1,2,3,4,5,6,7,8,9,10,11,12]
      context={'form':f,'log':l,"month":month,"id":id}
      return render(request,'meal/multiadd.html',context=context)








def signin(request):
    if request.method=='POST':

        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)


        if user is not None:
            if user.is_active:
                # return HttpResponse(user.groups.filter (name='meal-manager').exists())
                i=user.groups.filter (name='meal-manager').exists()
                if i== True:
                    # print('heeeeeeeeeeeeeeeeeeeeeeeeeeee')
                    login(request,user)
                    return redirect('home')
                else:
                    # request.session.set_expiry(120)#2 mintues por session expire
                    # request.session.get_expire_at_browser_close()
                    login(request,user)

                    u=User.objects.get(username=username).id

                    eid=Employee.objects.filter(user=u).values('id')
                    if not eid:
                        return HttpResponse('User is not an employee')
                    eid=eid[0]['id']

                    # return HttpResponse(eid)
                    return HttpResponseRedirect(reverse('multiadd',args=(eid,)))
                    # return HttpResponseRedirect('meal/multiadd/%d'%eid)


            else:
                return HttpResponse("Invalid user")
        else:
            return HttpResponse('invalid log in')
    else:
        # Session.objects.all().delete()
        # logout(request)
        return render(request, 'meal/signin.html')

def signout(request):
    logout(request)
    return redirect('signin')