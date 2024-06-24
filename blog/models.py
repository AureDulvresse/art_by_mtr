from django.db import models
from django.urls import reverse
from store.models import Artwork

# Create your models here.
class Post(models.Model):
    title = models.CharField(
        max_length=180, 
        unique=True, 
        verbose_name="Thème de l'événement"
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
    )
    description = models.TextField(verbose_name="Description")
    content = models.TextField(verbose_name="Contenu")
    event_date = models.DateTimeField(verbose_name="Date de l'événement")
    event_place = models.CharField(
        max_length=200, 
        verbose_name="Lieu de l'événement"
    )
    event_artworks = models.ManyToManyField(
        Artwork, 
        blank=True, 
        verbose_name="Œuvres de l'événement"
    )
    thumbnail = models.ImageField(
        upload_to="posts", 
        blank=True, 
        null=True, 
        verbose_name="Miniature"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Créé le"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Mis à jour le"
    )

    class Meta:
        db_table = "blog_post"
        ordering = ["title"]
        unique_together = ["title", "slug"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug})
