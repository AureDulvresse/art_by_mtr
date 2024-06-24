from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from store.utils import get_cart_items

from blog.models import Post
from store.models import Cart

# Create your views here.
def blog_page(request):
    posts = Post.objects.all().order_by("-updated_at")

    cart_items = None
    user = request.user
    if user.is_authenticated:
        try:
            cart, _ = get_cart_items(user)
            cart_items = cart.select_related('artwork').order_by('-updated_at')
        except Cart.DoesNotExist:
            cart = None

    paginator = Paginator(posts, settings.ELEMENTS_PER_PAGE)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'preview_cart_items': cart_items[:3] if cart_items else None,
    }

    return render(request, 'blog/pages/home.html', context)


def post_detail_page(request, slug) -> HttpResponse:

    cart_items = None
    user = request.user
    if user.is_authenticated:
        try:
            cart, _ = get_cart_items(user)
            cart_items = cart.select_related('artwork').order_by('-updated_at')
        except Cart.DoesNotExist:
            cart = None

    post = get_object_or_404(Post, slug=slug)
    
    on_coming_events = Post.objects.exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'on_coming_events': on_coming_events,
        'preview_cart_items': cart_items[:3] if cart_items else None,
    }

    return render(request, 'blog/pages/post-detail.html', context)

