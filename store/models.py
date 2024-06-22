from django.db import models
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
        db_table = "store_category"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Medium(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Medium"
        verbose_name_plural = "Media"
        db_table = "store_medium"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Artwork(models.Model):
    title = models.CharField(max_length=180, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
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

    class Meta:
        db_table = "store_artwork"
        ordering = ["title"]
        unique_together = ["title", "slug"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("artwork-detail", kwargs={"slug": self.slug})

class Order(models.Model):
    uuid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='order', alphabet='abcdefghijklmnopqrstuvwxyz1234567890')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ordered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "store_order"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer.username} ordered {self.quantity} of {self.artwork.title}"
    
    def get_total_price(self):
        return self.artwork.price * self.quantity

class Cart(models.Model):
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "store_cart"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Cart of {self.customer.username}"
    
    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_at = timezone.now()
            order.save()
        self.orders.clear()
        super().delete(*args, **kwargs)

class CheckOut(models.Model):
    uuid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet='abcdefghijklmnopqrstuvwxyz1234567890')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "CheckOut"
        db_table = "store_checkout"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Checkout by {self.customer.username}"

# class Payment(models.Model):
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Completed', 'Completed'),
#         ('Failed', 'Failed'),
#         ('Refunded', 'Refunded'),
#     ]

#     currency = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     status = models.CharField(max_length=15, choices=STATUS_CHOICES)
#     checkout = models.ForeignKey(CheckOut, on_delete=models.CASCADE)

#     class Meta:
#         db_table = "store_payment"
#         ordering = ["-created_at"]

#     def __str__(self):
#         return f'Payment {self.id} by {self.checkout.customer.username}'

