from django.shortcuts import get_object_or_404
from .models import Cart

def get_cart_items(user):
    cart = get_object_or_404(Cart, customer=user)
    orders = cart.orders.all()
    total_cost = cart.total_cost
    return orders, total_cost
