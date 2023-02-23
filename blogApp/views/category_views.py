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

#Category
@login_required
def category_mgt(request):
    categories = Category.objects.all()
    context['page_title'] = "Category Management"
    context['categories'] = categories
    return render(request, 'category_mgt.html',context)

@login_required
def manage_category(request,pk=None):
    # category = Category.objects.all()
    if pk == None:
        category = {}
    elif pk > 0:
        category = Category.objects.filter(id=pk).first()
    else:
        category = {}
    context['page_title'] = "Manage Category"
    context['category'] = category

    return render(request, 'manage_category.html',context)

@login_required
def save_category(request):
    resp = { 'status':'failed' , 'msg' : '' }
    if request.method == 'POST':
        category = None
        if not request.POST['id'] == '':
            category = Category.objects.filter(id=request.POST['id']).first()
        if not category == None:
            form = SaveCategory(request.POST,instance = category)
        else:
            form = SaveCategory(request.POST)
    if form.is_valid():
        form.save()
        resp['status'] = 'success'
        messages.success(request, 'Category has been saved successfully')
    else:
        for field in form:
            for error in field.errors:
                resp['msg'] += str(error + '<br>')
        if not category == None:
            form = SaveCategory(instance = category)
       
    return HttpResponse(json.dumps(resp),content_type="application/json")

@login_required
def delete_category(request):
    resp={'status' : 'failed', 'msg':''}
    if request.method == 'POST':
        id = request.POST['id']
        try:
            category = Category.objects.filter(id = id).first()
            category.delete()
            resp['status'] = 'success'
            messages.success(request,'Category has been deleted successfully.')
        except Exception as e:
            raise print(e)
    return HttpResponse(json.dumps(resp),content_type="application/json")

def categories(request):
    categories = Category.objects.filter(status = 1).all()
    context['page_title'] = "Category Management"
    context['categories'] = categories
    return render(request, 'categories.html',context)
