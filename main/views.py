import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            response = JsonResponse({'success': True, 'redirect_url': reverse("main:show_main")})
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        
        return JsonResponse({'success': False, 'error': 'Invalid username or password'})

    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Your account has been successfully created!'})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})

    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)    

    context = {
        'name': request.user.username,
        'class': 'PBP B',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)

def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product_entry = form.save(commit=False)
            product_entry.user = request.user
            product_entry.save()  # Save the product to the database

            # Return success response
            return JsonResponse({'success': True, 'message': 'Product created successfully!', 'redirect_url': '/products/'})
        else:
            # Return form errors if any
            return JsonResponse({'success': False, 'error': form.errors})

    else:
        form = ProductForm()
    
    context = {'form': form}
    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    products = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'user_id': product.user.id if product.user else None,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
        }
        for product in products
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, product_id):
   try:
       product_item = Product.objects.filter(pk=product_id)
       xml_data = serializers.serialize("xml", product_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Product.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related('user').get(pk=product_id)
        data = {
            'id': str(product.id),
            'user_id': product.user.id if product.user else None,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'user_username': product.user.username if product.user else None,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Product not found'}, status=404)

@csrf_exempt
@require_POST
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()

            # Return success response
            return JsonResponse({'success': True, 'message': 'Product updated successfully!', 'redirect_url': '/products/'})
        else:
            # Return form errors if any
            return JsonResponse({'success': False, 'error': form.errors})

    else:
        form = ProductForm(instance=product)

    context = {'form': form}
    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == "DELETE":
        product.delete()
        return JsonResponse({'success': True, 'message': 'Product deleted successfully!', 'redirect_url': '/products/'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    # Ambil data dari request POST
    name = request.POST.get("name")
    description = request.POST.get("description")
    price = request.POST.get("price")
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'  # Menangani checkbox
    user = request.user

    # Buat objek Product baru
    new_product = Product(
        name=name,
        description=description,
        price=price,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user,
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
def edit_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            updated = form.save()
            return JsonResponse({
                "id": str(updated.id),
                "name": updated.name,
                "brand": updated.brand,
                "price": updated.price,
                "rating": updated.rating,
                "category": updated.category,
                "thumbnail": updated.thumbnail,
                "description": updated.description,
                "is_featured": updated.is_featured,
            })
    return JsonResponse({"error": "Invalid request"}, status=400)