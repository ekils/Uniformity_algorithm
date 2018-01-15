#coding=utf-8


from django.shortcuts import render_to_response
from restaurants.models import Restaurant
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, HttpResponseRedirect
from restaurants.models import Restaurant, Food, Comment

import datetime

def menu(request,idd):
    if idd:
        r = Restaurant.objects.get(id=idd)
        print(r.id)
        return render_to_response('menu.html',locals())
    else:
        print('bull shit')
        return HttpResponseRedirect("/restaurants_list/")

@csrf_exempt
def welcome(request):
    if 'user_name' in request.POST:
        return HttpResponse('Welcome!~'+request.POST['user_name'])
    else:
        return render_to_response('welcome.html',locals())


@csrf_exempt
def list_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render_to_response('restaurants_list.html', locals())


def comment(request,idd):
    if idd:
        r = Restaurant.objects.get(id=idd)
    else:
        return HttpResponseRedirect("/restaurants_list/")

    errors= []
    if 'ok' in request.POST:
        user = request.POST['user']
        content = request.POST['content']
        email = request.POST['email']
        date_time = datetime.datetime.now()     # 擷取現在時間

        if not user or not content or not email:
            errors.append('* 有空白欄位，請不要留空')
        if '@' not in email:
            errors.append('* email格式不正確，請重新輸入')
        if not errors:
            Comment.objects.create(user=user, email=email, content=content, date_time=date_time, restaurant=r)
    return render_to_response('comments.html',locals())