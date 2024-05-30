from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
@renderer_classes([JSONRenderer, TemplateHTMLRenderer])
def get_data(request):
    person = {'name': 'Tim', 'age': 24}
    return Response({'person': person}, template_name='index.html')