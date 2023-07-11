from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.signin, name="signin" ),
    path('register/', views.register, name="register" ),
    path('home', views.home, name="home" ),
]