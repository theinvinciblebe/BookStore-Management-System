from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home(request):
    response = render(request, 'shop/base.html')
    print(type(response))  # This should output <class 'django.http.response.HttpResponse'>
    return response

