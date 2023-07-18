from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import Users
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.contrib.auth.hashers import make_password



def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(password)
        user = authenticate(request, email=email, password=password)
        print(email)
        print('this user',user)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
           return render(request, 'login.html', {'message': "Invalid password or email"})
        
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_pass = request.POST['confirm_pass']
        
        if len(password) < 8:
           return render(request, 'register.html',  {'message': "Passwords should be atleast 8 length"})
                                                     
        if password != confirm_pass:
            return render(request, 'register.html', {'message': "Passwords do not match"})
        
        if password.isdigit():
            return render(request, 'register.html', {'message': "Passwords do not match"})
        # creating new users
        user = Users(name=username, email=email, password=password)
        user.save()

        return redirect('signin')
    return render(request, 'register.html')

def log_out(request):
    logout(request)
    return redirect ('signin')


User = get_user_model()

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('forget-password')

        # Generate a unique token for password reset
        token = str(uuid.uuid4())
        user.reset_token = token
        user.save()

        # Construct the reset link
        reset_link = request.build_absolute_uri(f'/reset-password/{token}')

        # Send password reset email to the user with the reset link
        subject = 'Password Reset'
        message = f'Click the link below to reset your password:\n{reset_link}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email]
        send_mail(subject, message, from_email, to_email)

        return render(request, 'forget-password.html',  {'message': "Password reset link has been sent to your email."})

        # return redirect('')

    return render(request, 'forget-password.html')


def reset_password(request, token):
    if request.method == 'POST':
        password = request.POST.get('resetpassword')
        confirm_password = request.POST['Confirm_password']

        if password != confirm_password:
            return render(request, 'register.html', {'message': "Passwords do not match"})

        try:
            user = User.objects.get(reset_token=token)
        except User.DoesNotExist:
            messages.error(request, 'Invalid password reset link.')
            return redirect('signin')

        # user.set_password(password)
        # user.reset_token = None
        # user.save()

          # Hash the new password
        hashed_password = make_password(password)
        user.password = hashed_password
        user.reset_token = None
        user.save()
         # Update the user's session with the new password hash
        update_session_auth_hash(request, user)

        messages.success(request, 'Password has been reset. You can now log in with your new password.')
        return redirect('signin')

    return render(request, 'reset_password.html')

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')


def home(request):
    return render(request, 'home.html')