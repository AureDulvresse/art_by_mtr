from django.contrib import admin
from store.models import Payment

# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('checkout__customer__username',)  # Recherche par nom d'utilisateur du client
    readonly_fields = ('created_at', 'updated_at')  # Champs en lecture seule

    def has_delete_permission(self, request, obj=None):
        return False  # Désactiver la suppression via l'interface admin

    def has_add_permission(self, request):
        return False  # Désactiver l'ajout via l'interface admin

    def has_change_permission(self, request, obj=None):
        return False  # Désactiver la modification via l'interface admin

    # Optionnel : Personnalisation du titre de l'objet dans l'interface admin
    def __str__(self):
        return f'Payment {self.id}'
