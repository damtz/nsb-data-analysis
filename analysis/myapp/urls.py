from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name="signin" ),
    path('register/', views.register, name="register" ),
    path('home', views.home, name="home" ),
    path('logout', views.log_out, name='logout'),
]