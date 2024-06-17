from django.contrib import admin
from .models import Category, Medium, Artwork, Order, Cart, CheckOut
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

# Importer le modèle Customer si nécessaire
Customer = get_user_model()

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')

@admin.register(Medium)
class MediumAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'medium', 'price', 'stock', 'created_at', 'updated_at')
    list_filter = ('category', 'medium', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}  # Auto-generate slug from title

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'customer', 'artwork', 'quantity', 'ordered', 'created_at', 'ordered_at')
    list_filter = ('ordered', 'created_at', 'ordered_at')
    search_fields = ('customer__username', 'artwork__title')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at')
    search_fields = ('customer__username',)
    filter_horizontal = ('orders',)  # For ManyToManyField

@admin.register(CheckOut)
class CheckOutAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'customer', 'created_at')
    filter_horizontal = ('orders',)  # For ManyToManyField
    search_fields = ('customer__username',)
