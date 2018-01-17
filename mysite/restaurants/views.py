#coding=utf-8


from django.shortcuts import render_to_response
from restaurants.models import Restaurant
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, HttpResponseRedirect
from restaurants.models import Restaurant, Food, Comment
from restaurants.forms import CommentForm

from django.contrib.sessions.models import Session

import datetime

from django.contrib import auth  # 別忘了import auth


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/index/')
    else:
        return render_to_response('login.html')

def index(request):
    return render_to_response('index.html',locals())


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

    request.session['restaurants'] = restaurants

    return render_to_response('restaurants_list.html', locals())


def comment(request,idd):
    if idd:
        r = Restaurant.objects.get(id=idd)
    else:
        return HttpResponseRedirect("/restaurants_list/")

    # errors= []
    print(request.POST)
    if 'ok' in request.POST:
        print('okokok')
        f = CommentForm(request.POST)

        if f.is_valid():
            user = request.POST['user']
            content = request.POST['content']
            email = request.POST['email']
            date_time = datetime.datetime.now()     # 擷取現在時間

            c = Comment.objects.create(user=user, email=email, content=content, date_time=date_time, restaurant=r)
            c.save()
            f = CommentForm()
    else:
        print('not ok , not ok , not ok  ')
        f = CommentForm()
    return render_to_response('comments.html',locals())



def session_test(request):
    sid = request.COOKIES['sessionid']
    s = Session.objects.get(pk=sid)
    s_info = 'Session ID:' + sid + '<br>Expire_date:' + str(s.expire_date) + '<br>Data:' + str(s.get_decoded())
    return HttpResponse(s_info)