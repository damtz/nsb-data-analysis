from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name="signin" ),
    path('register/', views.register, name="register" ),
    path('home', views.home, name="home" ),
    path('logout', views.log_out, name='logout'),
    path('reset-password/<str:token>/', views.reset_password, name='reset-password'),
    path('forgotpassword', views.forget_password, name='forgetpassword'),
    path('password-reset-complete/', views.password_reset_complete, name='password_reset_complete'),
]

