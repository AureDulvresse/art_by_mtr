from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from art_by_mtr.settings import ELEMENTS_PER_PAGE
from store.models import Artwork, Cart, Order


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

    return render(request, "store/pages/contact.html")


@csrf_exempt
@login_required
def add_to_cart(request):
    if request.method == "POST":
        artwork_id = request.POST.get("artwork_id")
        quantity = int(request.POST.get("quantity", 1))

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