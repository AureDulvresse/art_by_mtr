from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

import json

from store.models import Artwork, CheckOut
from manager.forms import ArtworkForm

# Create your views here.

@login_required
def dashboard_page(request) -> HttpResponse:
    artworks = Artwork.objects.all().order_by('-updated_at')[:6]
    orders = CheckOut.objects.all().order_by('-created_at')[:6]

    context = {
        "artworks": artworks,
        "orders": orders,
    }
    return render(request, 'manager/pages/dashboard.html', context)


class ArtworkController:

    @login_required
    def index(request) -> HttpResponse:
        artworks = Artwork.objects.all().order_by('-updated_at')


        paginator = Paginator(artworks, 10)
        page = request.GET.get('page')
        artworks = paginator.get_page(page)

        context = {"artworks" : artworks }
        
        return render(request, 'manager/pages/artwork.html', context)
    
    @csrf_exempt
    @login_required
    def store(request):
        if request.method == 'POST':
            form = ArtworkForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Oeuvre ajoutée')
                return redirect('manager:artwork-list') 
        else:
            form = ArtworkForm()
    
    def show(request) -> HttpResponse:
        pass

    def update(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            artwork_id = data.get("artwork_id")
            artwork = Artwork.objects.get(pk = artwork_id)
            form = ArtworkForm(request.POST, instance = artwork)
            if form.is_valid():
                form.save()
                messages.success(request, 'Oeuvre modifiée')
                return redirect('manager:artwork_page') 
        else:
            form = ArtworkForm(instance = artwork)
        
        return render(request, 'manager/artwork_add_form_page.html', {'form': form})