from django.urls import path
# from django.conf.urls import handler404

from manager import views

app_name = "manager"

urlpatterns = [
   path('', views.dashboard_page, name = 'dashboard'),
   path('artworks/', views.ArtworkController.index, name = 'artwork-page'),
   
    # path('events/', views.event_page, name = 'event_page'),
    # path('events_form', views.event_form_page, name = 'event_form_page'),
    # path('events_add_form', views.event_add_form_page, name = 'event_add_form_page'),
    # path('orders', views.order_page, name = 'order_page'),
    # path('payments', views.payment_page, name = 'payment_page'),
    # path('seetings', views.seetings_page, name = 'seetings_page'),
    # path('delete_event/<int:event_id>/', views.delete_event, name = 'delete_event'),
    # path('delete_artwork/<int:artwork_id>/', views.delete_artwork, name = 'delete_artwork'),
    # path('create_event', views.create_event, name = 'create_event'),
    # path('create_artwork', views.create_artwork, name = 'create_artwork'),
    # path('edit_event/<int:event_id>', views.edit_event, name = 'edit_event'),
    # path('edit_artwork/<int:artwork_id>', views.edit_artwork, name = 'edit_artwork'),

]
# handler404 = f"{app_name}.views.page_404"