from django.urls import path
# from django.conf.urls import handler404

from manager import views

app_name = "manager"

urlpatterns = [
   path('', views.dashboard_page, name = 'dashboard'),

   path('artworks/', views.ArtworkController.index, name = 'artwork-list'),
   path('artworks/<str:artwork_id>/details/', views.ArtworkController.show, name = 'artwork-detail'),
   path('artworks/update/', views.ArtworkController.update, name = 'update-artwork'),
   path('artworks/delete/', views.ArtworkController.destroy, name = 'delete-artwork'),

   path('posts/', views.PostController.index, name = 'post-list'),
   path('artworks/', views.PostController.show, name = 'post-detail'),
   path('artworks/', views.ArtworkController.store, name = 'create-post'),
   path('artworks/', views.ArtworkController.update, name = 'update-post'),
   path('artworks/', views.ArtworkController.destroy, name = 'delete-post'),

   path('artworks/', views.ArtworkController.index, name = 'orders'),
   path('artworks/', views.ArtworkController.index, name = 'payments'),
   path('artworks/', views.ArtworkController.index, name = 'settings'),
]

# handler404 = f"{app_name}.views.page_404"