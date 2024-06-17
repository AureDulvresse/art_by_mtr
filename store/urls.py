from django.urls import path
# from django.conf.urls import handler404

from store import views

app_name = "store"

urlpatterns = [
   path('', views.home_page, name="home"),
   path('about/', views.about_page, name="about"),
   path('gallery/', views.gallery_page, name="gallery"),
   path('artwork/<str:slug>/', views.artwork_detail_page, name="artwork-detail"),
   path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
   path('contact/', views.contact_page, name="contact"),
]

# handler404 = f"{app_name}.views.page_404"