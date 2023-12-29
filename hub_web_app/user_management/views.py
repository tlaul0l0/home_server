from django.shortcuts import render

def get_login(request):
    return render(request, 'login.html')

def get_logout(request):
    return render(reqest, 'dashboard.html')