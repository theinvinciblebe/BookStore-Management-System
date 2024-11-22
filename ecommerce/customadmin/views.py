from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
# Products
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from django.shortcuts import render
from shop.models import Product, Category
from django.core.paginator import Paginator

from .models import Category


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def test_view(request):
    return HttpResponse("This is a protected page.")

# @login_required
# def admin_site(request):
#     context = {"page": "dashboard1"}
#     return render(request, 'customadmin/base.html', context)

@login_required
def dashboard2(request):
    context = {"page": "dashboard2"}
    return render(request, 'customadmin/base2.html', context)

@login_required
def dashboard3(request):
    context = {"page": "dashboard3"}
    return render(request, 'customadmin/base3.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            # Redirect to appropriate dashboard based on user role
            if user.is_staff:
                return redirect('product_list')
            return redirect('dashboard2')
        else:
            return render(request, 'customadmin/login.html', {'error': 'Invalid credentials'})

    # Render the login page if not a POST request
    return render(request, 'customadmin/login.html')


@login_required
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(products, 5)  # Show 5 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page": "product_list",
        "products": page_obj,  # Update this to page_obj to use paginated data
        "categories": categories,
        "page_obj": page_obj,  # Add page_obj to the context
    }
    return render(request, 'customadmin/product_list.html', context)


@login_required
def product_add(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'customadmin/product_add.html', {'form': form, 'categories': categories})



@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()  # Fetch all categories

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'customadmin/product_edit.html', {'form': form,'product': product, 'categories': categories})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'customadmin/product_confirm_delete.html', {'product': product})
