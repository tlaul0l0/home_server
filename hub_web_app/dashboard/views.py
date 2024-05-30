from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def get_data(request):
    person = {'name': 'Tim', 'age': 24}
    return Response(person)