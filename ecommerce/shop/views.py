from django.shortcuts import render
from django.http import HttpResponse
from shop.models import Product
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    context = {"page": "home"}
    response = render(request, 'shop/base.html', context)
    #print(type(response))  # This should output <class 'django.http.response.HttpResponse'>
    return response


# def shop(request):
#     context = {"page": "shop"}
#     response = render(request, 'shop/navbar-items-shop.html', context)
#     #print(type(response))  # This should output <class 'django.http.response.HttpResponse'>
#     return response

def shop(request):
    products = Product.objects.all()  # Fetch all products
    paginator = Paginator(products, 6)  # Show 6 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'products': page_obj,  # Paginated products
        'page_obj': page_obj,   # Page object for pagination
    }
    return render(request, 'shop/navbar-items-shop.html', context)

def shopdetail(request):
    context = {"page": "shopdetail"}
    response = render(request, 'shop/navbar-items-shopdetail.html', context)
    #print(type(response))  # This should output <class 'django.http.response.HttpResponse'>
    return response
