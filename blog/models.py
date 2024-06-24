from django.db import models
from django.urls import reverse
from store.models import Artwork

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=180, unique=True, verbose_name="Thème de l'évenement")
    slug = models.SlugField(max_length=250,unique=True)
    description = models.TextField()
    content = models.TextField()
    event_date = models.DateTimeField()
    event_place = models.CharField(max_length=200)
    event_artworks = models.ManyToManyField(Artwork)
    thumbnail = models.ImageField(upload_to="posts", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "blog_post"
        ordering = ["title"]
        unique_together = ["title", "slug"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug})