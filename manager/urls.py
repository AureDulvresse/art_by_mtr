from django.urls import path
# from django.conf.urls import handler404

from manager import views

app_name = "manager"

urlpatterns = [
   path('', views.dashboard_page, name = 'dashboard'),
   path('artworks/', views.ArtworkController.index, name = 'artworks'),
   path('artworks/<str:artwork_id>/details/', views.ArtworkController.show, name = 'artwork-detail'),
   path('artworks/delete/', views.ArtworkController.destroy, name = 'delete-artwork'),
   path('artworks/', views.ArtworkController.index, name = 'artworks'),
   path('artworks/', views.ArtworkController.index, name = 'events'),
   path('artworks/', views.ArtworkController.index, name = 'orders'),
   path('artworks/', views.ArtworkController.index, name = 'payments'),
   path('artworks/', views.ArtworkController.index, name = 'settings'),
]

# handler404 = f"{app_name}.views.page_404"