from dj_shop_cart.cart import Cart
from django.shortcuts import get_object_or_404, redirect, render
from apps.myapp.models import Product

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to the Django Shop!</h1>")
