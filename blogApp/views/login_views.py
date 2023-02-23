from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import json, datetime
from django.contrib.auth.models import User
from django.contrib import messages
from blogApp.models import UserProfile,Category, Post
import requests
import markdown
import base64
from datetime import datetime
from backports.zoneinfo import ZoneInfo
from django.http import JsonResponse
from blogApp.forms import UpdateProfile, UpdateProfileMeta, UpdateProfileAvatar, SaveCategory, SavePost, AddAvatar
from .token import token

category_list = Category.objects.exclude(status = 2).all()
context = {
    'page_title' : 'Simple Blog Site',
    'category_list' : category_list,
    'category_list_limited' : category_list[:3]
}

#login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

def home(request):
    context['page_title'] = 'Home'
    print(request.user)
    return render(request, 'home.html',context)

def git_home(request):
    from IPython.display import HTML, display
    content = {}
    url = 'https://api.github.com/gists/4239e01e668719e2ba1eddb08d0e7b60'
    headers = {"Accept": "application/vnd.github+json", "Authorization": token }
    response = requests.get(url, headers=headers)
    response_json = response.json()
    name = next(iter(response_json['files']))
    git = response_json['files'][name]['content']
    git = markdown.markdown(git, extensions=['markdown.extensions.extra', 'markdown.extensions.smarty'])
    content['git'] = git
    return JsonResponse(content)

def weather(request):
    content = {}
    url = 'http://api.openweathermap.org/data/2.5/weather?'
    api_key = "af78b062b7068b1667494cc118fcd076"
    city_name = 'seoul'
    complete_url = url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    list_of_data = response.json()
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' '
                    + str(list_of_data['coord']['lat']),
        "temp": str(int(list_of_data['main']['temp'] - 273.15)) + ' °C',
        "feel_temp": str(int(list_of_data['main']['feels_like'] - 273.15)) + ' °C',
        "cloud": str(list_of_data['clouds']['all']),
        "humidity": str(list_of_data['main']['humidity']) + '%',
        "description": str(list_of_data['weather'][0]['description'])
        }

    return JsonResponse(data)

@login_required
def profile(request):
    context = {
        'page_title':"My Profile"
    }

    return render(request,'profile.html',context)
    
@login_required
def update_profile(request):
    context['page_title'] = "Update Profile"
    user = User.objects.get(id= request.user.id)
    profile = UserProfile.objects.get(user= user)
    context['userData'] = user
    context['userProfile'] = profile
    if request.method == 'POST':
        data = request.POST
        form = UpdateProfile(data, instance=user)
        if form.is_valid():
            form.save()
            form2 = UpdateProfileMeta(data, instance=profile)
            if form2.is_valid():
                form2.save()
                messages.success(request,"Your Profile has been updated successfully")
                return redirect("profile")
            else:
                context['form2'] = form2
        else:
            context['form1'] = form
            form = UpdateProfile(instance=request.user)
    return render(request,'update_profile.html',context)


@login_required
def update_avatar(request):
    context['page_title'] = "Update Avatar"
    user = User.objects.get(id= request.user.id)
    context['userData'] = user
    context['userProfile'] = user.profile
    img = user.profile.avatar.url

    context['img'] = img
    if request.method == 'POST':
        form = UpdateProfileAvatar(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Profile has been updated successfully")
            return redirect("profile")
        else:
            context['form'] = form
            form = UpdateProfileAvatar(instance=user)
    return render(request,'update_avatar.html',context)
