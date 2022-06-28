"""SocialNetwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import  LoginView, HomeView,get_posts,LogoutView, RegisterView,PostCreateView,PostDetailView,VotePostView

app_name = 'account'
urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('get_post/', get_posts.as_view(), name="get_post"),
    path('register/', RegisterView.as_view(), name="register"),

    path('post_create/', PostCreateView.as_view(), name="post_create"),
    path('post_detail/<str:pk>/', PostDetailView.as_view(), name="post_detail"),
    path('vote_post/', VotePostView.as_view(), name="vote_post"),
]
