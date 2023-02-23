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

from blogApp.forms import UpdateProfile, UpdateProfileMeta, UpdateProfileAvatar, SaveCategory, SavePost, AddAvatar

category_list = Category.objects.exclude(status = 2).all()
context = {
    'page_title' : 'Simple Blog Site',
    'category_list' : category_list,
    'category_list_limited' : category_list[:3]
}

def page_not_found(request, exception):
    return render(request, 'error/404.html', context)

def server_error(request):
    return render(request, 'error/500.html', context)