import datetime
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
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
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

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
@login_required
def edit_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            updated = form.save()
            return JsonResponse({
                "name": updated.name,
                "description": updated.description,
                "price": updated.price,
                "category": updated.category,
                "thumbnail": updated.thumbnail,
                "is_featured": updated.is_featured,
            })
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
@csrf_exempt
def delete_product_ajax(request, id):
    if request.method == "POST":
        try:
            product = Product.objects.get(pk=id, user=request.user)
            product.delete()
            return JsonResponse({"success": True})
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "message": "Product not found"})
    return JsonResponse({"success": False, "message": "Invalid request"})

@csrf_exempt
@require_POST
def register_ajax(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success", "message": "Registration successful! You can now log in."}, status=201)
    else:
        return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    
@csrf_exempt
@require_POST
def login_ajax(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = JsonResponse({"status": "success", "message": "Login successful!"})
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
    else:
        return JsonResponse({"status": "error", "message": "Invalid username or password."}, status=401)
    
@login_required
def get_products_json(request):
    filter_type = request.GET.get("filter")

    if filter_type == "my":
        products = Product.objects.filter(user=request.user)
    else:
        products = Product.objects.all()

    data = [
        {
            "pk": product.pk,
            "fields": {
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "thumbnail": product.thumbnail,
                "category": product.get_category_display(),  # 💡 tampilkan "Jerseys", bukan "jersey"
                "is_featured": product.is_featured,
                "user": product.user.id if product.user else None,
            },
        }
        for product in products
    ]
    return JsonResponse(data, safe=False)

@login_required
def get_product_by_id_json(request, id):
    product = get_object_or_404(Product, pk=id)
    return JsonResponse(model_to_dict(product))