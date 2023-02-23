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

#Post
@login_required
def post_mgt(request):
    if request.user.profile.user_type == 1:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(author = request.user).all()

    context['page_title'] = "post Management"
    context['posts'] = posts
    return render(request, 'post_mgt.html',context)

@login_required
def manage_post(request,pk=None):
    # post = post.objects.all()
    if pk == None:
        post = {}
    elif pk > 0:
        post = Post.objects.filter(id=pk).first()
    else:
        post = {}
    context['page_title'] = "Manage post"
    context['post'] = post

    return render(request, 'manage_post.html',context)

@login_required
def save_post(request):
    resp = { 'status':'failed' , 'msg' : '' }
    if request.method == 'POST':
        post = None
        if not request.POST['id'] == '':
            post = Post.objects.filter(id=request.POST['id']).first()
        if not post == None:
            form = SavePost(request.POST,request.FILES,instance = post)
        else:
            form = SavePost(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        resp['status'] = 'success'
        messages.success(request, 'Post has been saved successfully')
    else:
        for field in form:
            for error in field.errors:
                resp['msg'] += str(error + '<br>')
        if not post == None:
            form = SavePost(instance = post)
       
    return HttpResponse(json.dumps(resp),content_type="application/json")

@login_required
def delete_post(request):
    resp={'status' : 'failed', 'msg':''}
    if request.method == 'POST':
        id = request.POST['id']
        try:
            post = Post.objects.filter(id = id).first()
            post.delete()
            resp['status'] = 'success'
            messages.success(request,'Post has been deleted successfully.')
        except Exception as e:
            raise print(e)
    return HttpResponse(json.dumps(resp),content_type="application/json")

def view_post(request,pk=None):
    context['page_title'] = ""
    if pk is None:
        messages.error(request,"Unabale to view Post")
        return redirect('home-page')
    else:
        post = Post.objects.filter(id = pk).first()
        context['page_title'] = post.title
        context['post'] = post
    return render(request, 'view_post.html',context)

def post_by_category(request,pk=None):
    if pk is None:
        messages.error(request,"Unabale to view Post")
        return redirect('home-page')
    else:
        category = Category.objects.filter(id=pk).first()
        context['page_title'] = category.name
        context['category'] = category
        posts = Post.objects.filter(category = category).all()
        context['posts'] = posts
    if category.name == 'Gist':
        gist_list = []

        context['gists'] = gist_list
    return render(request, 'by_categories.html',context)
