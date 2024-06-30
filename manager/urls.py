from django.urls import path
# from django.conf.urls import handler404

from manager import views

app_name = "manager"

urlpatterns = [
   path('', views.dashboard_page, name = 'dashboard'),

   path('artworks/create/', views.ArtworkController.store, name = 'add-artwork'),
   path('artworks/', views.ArtworkController.index, name = 'artwork-list'),
   path('artworks/update/<str:artwork_id>/', views.ArtworkController.update, name = 'update-artwork'),
   path('artworks/delete/', views.ArtworkController.destroy, name = 'delete-artwork'),

   path('posts/create/', views.PostController.store, name = 'add-post'),
   path('posts/', views.PostController.index, name = 'post-list'),
   path('posts/update/<str:post_id>/', views.PostController.update, name = 'update-post'),
   path('posts/delete/', views.PostController.destroy, name = 'delete-post'),

   path('orders/', views.ArtworkController.index, name = 'orders'),
   path('payments/', views.ArtworkController.index, name = 'payments'),
   path('settings/', views.ArtworkController.index, name = 'settings'),
]

# handler404 = f"{app_name}.views.page_404"