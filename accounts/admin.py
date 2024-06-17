from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer

# Définir un admin personnalisé pour Customer
@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    # Liste des champs à afficher dans l'interface d'administration
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
    # Liste des champs à filtrer dans l'interface d'administration
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    # Champs de recherche dans l'interface d'administration
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Champs pour l'ajout et la modification d'un utilisateur dans l'interface d'administration
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Champs à afficher lors de la création d'un nouvel utilisateur dans l'interface d'administration
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
