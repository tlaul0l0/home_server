from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def get_login(request):
    return render(request, 'login.html')

def get_register(request):
    return render(request, 'register.html')

def login_user(request, email, password):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return redirect("login")

def logout_user(request):
    logout(request)

def create_user(request, email, username, password, confirm_password):
    if request.method == "POST":
        email = request.POST['email']
        username = email
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if not password == confirm_password:
            pass

        user = User.objects.create_user(username, email, password)
        return redirect("dashboard")