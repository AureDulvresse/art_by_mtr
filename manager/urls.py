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

   path('orders/', views.OrderController.index, name = 'order-list'),
   path('orders/details/<str:order_number>', views.OrderController.show, name = 'order-detail'),

   path('payments/', views.payment_list, name = 'payments'),
   path('settings/', views.settings_page, name = 'settings'),

   path('settings/categories/add/', views.CategoryController.store, name='add-category'),
   path('settings/categories/edit/<int:id>/', views.CategoryController.update, name='edit-category'),
   path('settings/categories/delete/', views.CategoryController.destroy, name='delete-category'),

   path('settings/mediums/add/', views.MediumController.store, name='add-medium'),
   path('settings/mediums/edit/<int:id>/', views.MediumController.update, name='edit-medium'),
   path('settings/mediums/delete/', views.MediumController.destroy, name='delete-medium'),
]

# handler404 = f"{app_name}.views.page_404"