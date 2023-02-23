from .views import category_views, gist_views, login_views, post_views
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('', login_views.home, name="home-page"),
    path('git',login_views.git_home,name='git-home'),
    path('weather',login_views.weather,name='weather'),
    
    path('login',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user = True),name='login'),
    path('userlogin', login_views.login_user, name="login-user"),
    path('logout',login_views.logoutuser,name='logout'),
    path('profile',login_views.profile,name='profile'),
    path('update-profile',login_views.update_profile,name='update-profile'),
    path('update-avatar',login_views.update_avatar,name='update-avatar'),
    
    path('category_mgt',category_views.category_mgt,name='category-mgt'),
    path('manage_category',category_views.manage_category,name='manage-category'),
    path(r'manage_category/<int:pk>',category_views.manage_category,name='edit-category'),
    path('save_category',category_views.save_category,name='save-category'),
    path('delete_category',category_views.delete_category,name='delete-category'),
    path('categories',category_views.categories,name='category-page'),
    
    path('post_mgt',post_views.post_mgt,name='post-mgt'),
    path('manage_post',post_views.manage_post,name='manage-post'),
    path(r'manage_post/<int:pk>',post_views.manage_post,name='edit-post'),
    path('save_post',post_views.save_post,name='save-post'),
    path('delete_post',post_views.delete_post,name='delete-post'),
    path(r'view_post/<int:pk>',post_views.view_post,name='view-post'),
    path(r'<int:pk>',post_views.post_by_category,name='category-post'),
    
    path('git_post',gist_views.git_post,name='git-post'),
    path('gistlist',gist_views.gitpost,name='gitpost'),
    
]
