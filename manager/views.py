from datetime import datetime, timedelta
import json

from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.db.models import Count

from accounts.models import Customer
from store.models import Artwork, Category, CheckOut, Order
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
        'posts_this_month': Post.objects.filter(event_date__month=current_month.month).count(),
        'sales_current_month': sales_current_month,
        'sales_previous_month': sales_previous_month,
        'artwork_categories': artwork_categories,
        'artworks': artworks[:10],
    }

    return render(request, 'manager/pages/dashboard.html', context)


class OrderController:

    @staticmethod
    @login_required
    def index(request):
        orders = Order.objects.all().filter(ordered=True)

        paginator = Paginator(orders, 10)
        page = request.GET.get('page')
        orders = paginator.get_page(page)

        context = {
            'orders': orders,
        }

        return render(request, 'manager/pages/orders_list.html', context)

    @staticmethod
    @login_required
    def show(request, order_number):
        order = get_object_or_404(Order, uuid=order_number)

        context = {
            'orders': order,
        }

        return render(request, 'manager/pages/order_list.html', context)
    

class ArtworkController:

    @staticmethod
    @login_required
    def index(request):
        artworks = Artwork.objects.all().order_by('-updated_at')

        paginator = Paginator(artworks, 10)
        page = request.GET.get('page')
        artworks = paginator.get_page(page)

        context = {"artworks": artworks}
        
        return render(request, 'manager/pages/artwork_list.html', context)
    
    @staticmethod
    @csrf_exempt
    @login_required
    def store(request):
        if request.method == 'POST':
            form = ArtworkForm(request.POST, request.FILES)
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
    def update(request, artwork_id):
        artwork = get_object_or_404(Artwork, pk=artwork_id)

        if request.method == 'POST':
            form = ArtworkForm(request.POST, request.FILES, instance=artwork)
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
    @require_POST
    def destroy(request):
        try:
            data = json.loads(request.body)
            artwork_id = data.get('artwork_id')
            artwork = get_object_or_404(Artwork, pk=artwork_id)
            artwork.delete()
            return JsonResponse({'success': True, 'message': 'Œuvre supprimée avec succès'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Une erreur est survenue lors de la suppression de l\'œuvre'}, status=500)


class PostController:

    @staticmethod
    @login_required
    @csrf_exempt
    @staticmethod
    @csrf_exempt
    @login_required
    def store(request):
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Evènement créé')
                return redirect('manager:post-list') 
        else:
            form = PostForm()
        
        context = {'form': form}
        return render(request, 'manager/pages/post_add.html', context)

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
    def update(request, post_id):
        post = get_object_or_404(Post, pk=post_id)

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Evènement modifiée')
                return redirect('manager:post-list') 
        else:
            form = PostForm(instance=post) 
        
        context = {'form': form, 'post': post}
        return render(request, 'manager/pages/post_edit.html', context)

    @staticmethod
    @csrf_exempt
    @login_required
    @require_POST
    def destroy(request):
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')
            post = get_object_or_404(Post, pk=post_id)
            post.delete()
            return JsonResponse({'success': True, 'message': 'Evènement supprimé avec succès'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Une erreur est survenue lors de la suppression de l\'œuvre'}, status=500)