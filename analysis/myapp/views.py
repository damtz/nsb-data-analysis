from django.shortcuts import render, redirect
from myapp.models import Users
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login

# Create your views here.
# def signin(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']

#         try:
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 # error_message = 'Invalid username or password.'
#                 return render(request, 'login.html')
#         except Exception as e:
#             error_message = f"An error occurred: {str(e)}"
#             return render(request, 'error.html', {'error_message': error_message})

#     return render(request, 'login.html')

def signin(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, name=name, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return render(request, 'home.html') 
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
