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

def git_post(request):
    if request.method == "POST":
        id = request.POST['gist']
        url = 'https://api.github.com/gists/{}'.format(id)
        headers = {"Accept": "application/vnd.github+json"}
        response = requests.get(url, headers=headers)
        response_json = response.json()
        name = next(iter(response_json['files']))
        content = response_json['files'][name]['content']
        content = markdown.markdown(content, extensions=['markdown.extensions.extra', 'markdown.extensions.smarty'])
        update_date = datetime.strptime(response_json['updated_at'], '%Y-%m-%dT%H:%M:%S%z').astimezone(ZoneInfo('Asia/Seoul'))
        create_date = datetime.strptime(response_json['created_at'], '%Y-%m-%dT%H:%M:%S%z').astimezone(ZoneInfo('Asia/Seoul'))
        context['titlee'] = next(iter(response_json['files']))
        context['update_date'] = update_date
        context['create_date'] = create_date
        context['author'] = 'sjin1105'
        context['category'] = 'gist'
        context['blog_post'] = content
    return render(request, 'git_post.html',context)

def gitpost(request):
    gist_list = []
    content = {}
    url = 'https://api.github.com/gists'
    headers = {"Accept": "application/vnd.github+json", "Authorization": token}
    response = requests.get(url, headers=headers)
    gists = response.json()
    for gist in gists:
        gist_dict = {}
        gist_dict['name'] = next(iter(gist['files']))
        gist_dict['id'] = gist['id']
        if gist_dict['name'] != 'README.md':
            gist_list.append(gist_dict)
    content['gists'] = gist_list
    return JsonResponse(content)
