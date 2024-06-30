import os
import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Cart

def get_cart_items(user):
    cart = Cart.objects.get(customer = user)
    orders = cart.orders.all()
    total_cost = cart.total_cost
    return orders, total_cost

def get_unique_filename(instance, filename):
    extension = filename.split('.')[-1]
    filename = f"{instance.title}_{uuid.uuid4().hex[:8]}.{extension}"

    file_path = f'media/artworks/{filename}'

    return os.path.join(settings.BASE_DIR, file_path)