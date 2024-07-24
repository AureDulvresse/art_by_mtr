from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from django.template.loader import render_to_string
from django.utils.html import strip_tags

import json
import stripe

from store.models import Artwork, Cart, CheckOut, Order
from store.utils import get_cart_items
from blog.models import Post
from art_by_mtr.settings import PAYPAL_CLIENT_ID

stripe.api_key = settings.STRIPE_SECRET_KEY

# Fonction utilitaire pour obtenir les items du panier
def get_cart_items_preview(request):
    cart_items = None
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(customer=request.user)
            cart_items = cart.orders.select_related('artwork').order_by('-updated_at')
        except Cart.DoesNotExist:
            cart = None
    return cart_items

def home_page(request):
    artworks = Artwork.objects.all().order_by('-updated_at')[:3]
    posts = Post.objects.all().order_by('-updated_at')[:3]
    
    cart_items = get_cart_items_preview(request)

    context = {
        'artworks': artworks,
        'posts': posts,
        'preview_cart_items': cart_items[:3] if cart_items else None,
    }

    return render(request, 'store/pages/home.html', context)

def about_page(request):
    cart_items = get_cart_items_preview(request)
    context = {
        'preview_cart_items': cart_items[:3] if cart_items else None,
    }
    return render(request, "store/pages/about.html", context)

def gallery_page(request):
    artworks = Artwork.objects.all().order_by("-updated_at")

    cart_items = get_cart_items_preview(request)

    paginator = Paginator(artworks, settings.ELEMENTS_PER_PAGE)
    page = request.GET.get('page')
    artworks = paginator.get_page(page)

    context = {
        'artworks': artworks,
        'preview_cart_items': cart_items[:3] if cart_items else None,
    }

    return render(request, 'store/pages/gallery.html', context)

def artwork_detail_page(request, slug):
    cart_items = get_cart_items_preview(request)

    artwork = get_object_or_404(Artwork, slug=slug)
    current_category = artwork.category
    related_artworks = Artwork.objects.exclude(id=artwork.id).filter(category=current_category)[:3]
    
    context = {
        'artwork': artwork,
        'related_artworks': related_artworks,
        'preview_cart_items': cart_items[:3] if cart_items else None,
    }

    return render(request, 'store/pages/artwork-detail.html', context)

def contact_page(request) -> HttpResponse:
    cart_items = get_cart_items_preview(request)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validation des données du formulaire
        if not name or not email or not subject or not message:
            messages.error(request, "Tous les champs sont requis.")
            return redirect('store:contact')

        if '@' not in email or '.' not in email:
            messages.error(request, "Veuillez entrer une adresse email valide.")
            return redirect('store:contact')

        # Construire le message complet avec un formatage amélioré
        logo_url = request.build_absolute_uri('/static/img/logo_bg_white.png')
        html_message = render_to_string('store/components/contact_email.html', {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'logo_url': logo_url,
        })
        plain_message = strip_tags(html_message)

        try:
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  # Assurez-vous de définir cette variable dans vos settings
                fail_silently=False,
                html_message=html_message
            )
            messages.success(request, "Votre message a été envoyé avec succès!")
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite: {e}")

        return redirect('store:contact')

    context = {
        'preview_cart_items': cart_items[:3] if cart_items else None, 
    }
    
    return render(request, "store/pages/contact.html", context)

@login_required
def cart_page(request):
    user = request.user
    cart, total_cost = get_cart_items(user)

    context = {
        "cart": cart.select_related('artwork').order_by('-updated_at'),
        "total_cost": total_cost,
        'preview_cart_items': cart.select_related('artwork').order_by('-updated_at')[:3] if cart.exists() else None,
    }

    return render(request, "store/pages/cart.html", context)

@login_required
def checkout_page(request):
    user = request.user
    cart, total_cost = get_cart_items(user)

    if request.method == "POST":
        CheckOut.objects.create(customer=user, orders=cart)
        cart.delete()
        return redirect("store:shop")

    context = {
        'cart': cart,
        'total_cost': total_cost,
        'preview_cart_items': cart.select_related('artwork').order_by('-updated_at')[:3] if cart.exists() else None,
    }

    return render(request, "store/pages/checkout.html", context)

@csrf_exempt
@login_required
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        artwork_id = data.get("artwork_id")
        quantity = int(data.get("quantity"))

        try:
            artwork = Artwork.objects.get(id=artwork_id)
        except Artwork.DoesNotExist:
            return JsonResponse({"error": "Artwork not found"}, status=404)

        cart, _ = Cart.objects.get_or_create(customer=request.user)
        order, created = Order.objects.get_or_create(customer=request.user, artwork=artwork, ordered=False)

        if not created:
            order.quantity += quantity
        else:
            order.quantity = quantity

        order.save()
        cart.orders.add(order)
        
        cart_items = cart.orders.select_related('artwork').order_by('-updated_at')

        # Récupérer les données mises à jour du panier
        cart_items_html = render_to_string('store/partials/cart_items.html', {'preview_cart_items': cart_items[:3]})

        return JsonResponse({"message": "L'oeuvre a été ajouter au panier avec succès", 
                             "cart_items_html": cart_items_html}, 
                             status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_uuid = data.get('order_uuid')

        try:
            order = get_object_or_404(Order, uuid=order_uuid)
            cart = get_object_or_404(Cart, customer=request.user)

            if order in cart.orders.all():
                cart.orders.remove(order)
                order.delete()

                cart_items = cart.orders.select_related('artwork').order_by('-updated_at')

                # Récupérer les données mises à jour du panier
                cart_items_html = render_to_string('store/partials/cart_items.html', {'preview_cart_items': cart_items[:3]})
                cart_items_table_html = render_to_string('store/partials/cart_items_table.html', {'cart': cart_items})

                return JsonResponse({
                    'success': True, 
                    'cart_items_html': cart_items_html, 
                    'cart_items_table_html': cart_items_table_html,
                })
            else:
                return JsonResponse({'success': False, 'error': 'Order not in cart'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

    return JsonResponse({'success': False, 'error': 'User not authenticated'}, status=401)

# Code des paiements (Stripe, PayPal, etc.) peut être réactivé et ajusté si nécessaire
