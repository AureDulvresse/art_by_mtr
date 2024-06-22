from django.db import models
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse
from shortuuid.django_fields import ShortUUIDField
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name

class Medium(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Support"
        verbose_name_plural = "Supports"

    def __str__(self) -> str:
        return self.name

class Artwork(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=1)
    width = models.IntegerField()
    height = models.IntegerField()
    thumbnail = models.ImageField(upload_to="artworks", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self) -> HttpResponse:
        return reverse("artwork-detail", kwargs={"uuid": self.slug})

class Order(models.Model):
    uuid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='order', alphabet='abcdefghijklmnopqrstuvwxyz1234567890')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ordered_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.customer.username} commande {self.quantity} {self.artwork.title}"
    
    def get_total_price(self) -> int:
        return self.artwork.price * self.quantity

class Cart(models.Model):
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"Panier de {self.customer.username}"
    
    def delete(self, *args, **kwargs) -> None:
        for order in self.orders.all():
            order.ordered = True
            order.ordered_at = timezone.now()
            order.save()
        self.orders.clear()
        super(*args, **kwargs).delete()

class CheckOut(models.Model):
    uuid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='bill', alphabet='abcdefghijklmnopqrstuvwxyz1234567890')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commande"

    def __str__(self) -> str:
        return f"Commande de {self.customer.username}"

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    stripe_checkout_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)
    checkout = models.ForeignKey(CheckOut, on_delete=models.CASCADE)

    def __str__(self):
        return f'Payment {self.id} by {self.user}'
