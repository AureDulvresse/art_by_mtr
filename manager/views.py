from datetime import datetime, timedelta
import json

from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from django.db.models import Count, Prefetch, Q

from accounts.models import Customer
from store.models import Artwork, Category, CheckOut, Order, Payment
from blog.models import Post
from manager.forms import ArtworkForm, PostForm

# Fonction utilitaire pour obtenir le premier jour du mois
def first_day_of_month(date):
    return date.replace(day=1)

def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser

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

def payment_list(request):
    payments = Payment.objects.all().order_by('-created_at')

    # Gestion de la recherche
    query = request.GET.get('q')
    if query and query.strip():
        payments = payments.filter(checkout__customer__username__icontains=query)

    # Pagination
    paginator = Paginator(payments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'payments': page_obj,
        'query': query if query else '',
    }

    return render(request, 'manager/pages/payment_list.html', context)

class OrderController:

    @staticmethod
    @login_required
    @user_passes_test(is_staff_or_superuser)
    def index(request):
        query = request.GET.get('q')
        customers_with_orders = (
            Customer.objects.filter(is_staff=False, is_superuser=False)
            .annotate(order_count=Count('order', filter=Q(order__ordered=True)))
            .filter(order_count__gt=0)
        )

        if query:
            customers_with_orders = customers_with_orders.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query)
            )
            
        orders_prefetch = Prefetch('order_set', queryset=Order.objects.filter(ordered=True))
        customers = customers_with_orders.prefetch_related(orders_prefetch)

        context = {
            'customers': customers,
            'query': query,
        }

        return render(request, 'manager/pages/orders_list.html', context)

    @staticmethod
    @login_required
    @user_passes_test(is_staff_or_superuser)
    def show(request, order_number):
        order = get_object_or_404(Order, uuid=order_number, customer__is_staff=False, customer__is_superuser=False)

        context = {
            'order': order,
            'artwork': order.artwork,
        }

        return render(request, 'manager/pages/order_details.html', context)
    

class ArtworkController:

    @staticmethod
    @login_required
    def index(request):
        artworks = Artwork.objects.all().order_by('-updated_at')

        # Gestion de la recherche
        query = request.GET.get('q')
        if query and query.strip():
            artworks = artworks.filter(title__icontains=query)

        paginator = Paginator(artworks, 10)
        page = request.GET.get('page')
        artworks = paginator.get_page(page)

        context = {
            "artworks": artworks,
            "query": query if query else '',
        }

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

        # Gestion de la recherche
        query = request.GET.get('q')
        if query and query.strip():
            posts = posts.filter(title__icontains=query)

        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)

        context = {
            'posts': posts,
            'query': query if query else '',  # Retourne une chaîne vide si query est None
        }

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