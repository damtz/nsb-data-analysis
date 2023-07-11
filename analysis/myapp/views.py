from django.shortcuts import render, redirect
from myapp.models import Users
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        print(email)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            return JsonResponse({'message': 'login failed'})
        
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

def home(request):
    return render(request, 'home.html')
