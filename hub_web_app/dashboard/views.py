from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def get_dashboard(request):
    return render(request, 'dashboard.html')
