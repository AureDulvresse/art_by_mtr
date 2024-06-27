from datetime import datetime, timedelta
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.db.models import Count

from accounts.models import Customer
from store.models import Artwork, Category, CheckOut
from blog.models import Post
from manager.forms import ArtworkForm, PostForm

# Fonction utilitaire pour obtenir le premier jour du mois
def first_day_of_month(date):
    return date.replace(day=1)

@login_required
def dashboard_page(request):
    artworks = Artwork.objects.all()
    
    # Filtrer les ventes pour le mois en cours et le mois précédent
    today = datetime.today()
    current_month = first_day_of_month(today)
    previous_month = first_day_of_month(today - timedelta(days=1)).replace(day=1)

    sales_current_month = CheckOut.objects.filter(created_at__gte=current_month).count()
    sales_previous_month = CheckOut.objects.filter(created_at__gte=previous_month, created_at__lt=current_month).count()

    # Récupérer les catégories d'œuvres et compter le nombre d'œuvres par catégorie
    artwork_categories = Category.objects.annotate(artwork_count=Count('artwork')).order_by('-artwork_count')

    context = {
        'nb_artwork': artworks.count(),
        'artworks_sold_month': sales_current_month,
        'total_customers': Customer.objects.filter(is_superuser=False, is_staff=False, is_active=True).count(),
        'Posts_this_month': Post.objects.filter(event_date__month=current_month.month).count(),
        'sales_current_month': sales_current_month,
        'sales_previous_month': sales_previous_month,
        'artwork_categories': artwork_categories,
        'artworks': artworks[:10],
    }

    return render(request, 'manager/pages/dashboard.html', context)


class ArtworkController:

    @staticmethod
    @login_required
    def index(request):
        artworks = Artwork.objects.all().order_by('-updated_at')

        paginator = Paginator(artworks, 10)
        page = request.GET.get('page')
        artworks = paginator.get_page(page)

        context = {"artworks": artworks}
        
        return render(request, 'manager/pages/artwork.html', context)
    
    @staticmethod
    @csrf_exempt
    @login_required
    def store(request):
        if request.method == 'POST':
            form = ArtworkForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Œuvre ajoutée')
                return redirect('manager:artwork-list') 
        else:
            form = ArtworkForm()
        
        context = {'form': form}
        return render(request, 'manager/pages/artwork_add.html', context)
    
    @staticmethod
    @login_required
    def show(request, artwork_id):
        artwork = get_object_or_404(Artwork, id=artwork_id)
        context = {"artwork": artwork}
        return render(request, 'manager/pages/artwork_detail.html', context)
    
    @staticmethod
    @login_required
    def update(request, artwork_id):
        artwork = get_object_or_404(Artwork, pk=artwork_id)

        if request.method == 'POST':
            form = ArtworkForm(request.POST, instance=artwork)
            if form.is_valid():
                form.save()
                messages.success(request, 'Œuvre modifiée')
                return redirect('manager:artwork-list') 
        else:
            form = ArtworkForm(instance=artwork)
        
        context = {'form': form, 'artwork': artwork}
        return render(request, 'manager/pages/artwork_edit.html', context)
    
    @staticmethod
    @csrf_exempt
    @login_required
    def destroy(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            id = int(data.get('id'))

        if request.user.is_authenticated:
            
            try:
                artwork = get_object_or_404(Artwork, pk=id)
                artwork.delete()

                artwork_list = Artwork.objects.all().order_by('-updated_at')

                # Récupérer les données mises à jour du panier
                artwork_list_html = render_to_string('manager/partials/artwork_list.html', {'artworks': artwork_list})

                return JsonResponse({
                    'success': True, 
                    'artwork_list_html': artwork_list_html, 
                })
                    
            except Exception as e:
                return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

        return JsonResponse({'success': False, 'error': 'User not authenticated'}, status=401)


class PostController:

    @staticmethod
    @login_required
    @csrf_exempt
    def create(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save()
                data = {
                    'success': True,
                    'message': 'Événement ajouté avec succès',
                    'post_id': post.id,
                }
            else:
                data = {
                    'success': False,
                    'errors': form.errors,
                }
            return JsonResponse(data)

    @staticmethod
    @login_required
    @csrf_exempt
    def delete(request, post_id):
        if request.method == 'POST':
            try:
                post = Post.objects.get(pk=post_id)
                post.delete()
                data = {
                    'success': True,
                    'message': 'Événement supprimé avec succès',
                }
            except Post.DoesNotExist:
                data = {
                    'success': False,
                    'message': 'Événement non trouvé',
                }
            return JsonResponse(data)

    @staticmethod
    @login_required
    def update(request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                data = {
                    'success': True,
                    'message': 'Événement mis à jour avec succès',
                    'post_id': post.id,
                }
            else:
                data = {
                    'success': False,
                    'errors': form.errors,
                }
            return JsonResponse(data)
        else:
            form = PostForm(instance=post)
        
        context = {'form': form, 'post': post}
        return render(request, 'manager/pages/post_edit.html', context)

    @staticmethod
    @login_required
    def index(request):
        posts = Post.objects.all().order_by('-event_date')

        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)

        context = {'posts': posts}
        return render(request, 'manager/pages/post_list.html', context)

    @staticmethod
    @login_required
    def show(request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        context = {'post': post}
        return render(request, 'manager/pages/post_detail.html', context)
