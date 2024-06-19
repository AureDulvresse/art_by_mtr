from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from art_by_mtr.settings import ELEMENTS_PER_PAGE
from store.models import Artwork, Cart, Order

import json


def home_page(request) -> HttpResponse:
    artworks = Artwork.objects.all().order_by('-updated_at')[:3]

    context = {
        'artworks': artworks,
        'events': 4,
    }

    return render(request, 'store/pages/home.html', context)

def about_page(request) -> HttpResponse:
    context = {
        "testimonials": "testi",
    }

    return render(request, "store/pages/about.html", context)


def gallery_page(request) -> HttpResponse:
    artworks =  Artwork.objects.all().order_by("-updated_at")

    paginator = Paginator(artworks, ELEMENTS_PER_PAGE)
    page = request.GET.get('page')
    artworks = paginator.get_page(page)

    context = {
        'artworks': artworks,
    }

    return render(request, 'store/pages/gallery.html', context)


def artwork_detail_page(request, slug):

    artwork = get_object_or_404(Artwork, slug=slug)
    
    current_category = artwork.category
    
    related_artworks = Artwork.objects.exclude(id=artwork.id)
    
    related_artworks = related_artworks.filter(category=current_category)[:3]
    
    
    context = {
        'artwork': artwork,
        'related_artworks': related_artworks,
    }

    return render(request, 'store/pages/artwork-detail.html', context)

def contact_page(request) -> HttpResponse:
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validation simple des données du formulaire
        if not name or not email or not subject or not message:
            messages.error(request, "Tous les champs sont requis.")
            return redirect('store:contact')

        # Validation de l'adresse email
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

    return render(request, "store/pages/contact.html")


@csrf_exempt
@login_required
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        artwork_id = data.get("artwork_id")
        quantity = int(data.get("quantity", 1))

        print(request.POST.get("artwork_id"), artwork_id, type(artwork_id))

        try:
            artwork = Artwork.objects.get(id=artwork_id)
        except Artwork.DoesNotExist:
            return JsonResponse({"error": "Artwork not found"}, status=404)

        cart, created = Cart.objects.get_or_create(customer=request.user)
        order, created = Order.objects.get_or_create(customer=request.user, artwork=artwork, ordered=False)

        if not created:
            order.quantity += quantity
        else:
            order.quantity = quantity

        order.save()
        cart.orders.add(order)

        return JsonResponse({"message": "Artwork added to cart successfully", "quantity": order.quantity}, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)