import accounts
from django.urls import path
# from django.conf.urls import handler404

from store import views

app_name = "store"

urlpatterns = [
   path('', views.home_page, name="home"),
   path('about/', views.about_page, name="about"),
   path('gallery/', views.gallery_page, name="gallery"),
   path('artwork/<str:slug>/', views.artwork_detail_page, name="artwork-detail"),
   path('store/cart/', views.cart_page, name="cart"),
   path('store/add-to-cart/', views.add_to_cart, name='add-to-cart'),
   path('store/checkout/', views.checkout_page, name="checkout"),
   path('contact/', views.contact_page, name="contact"),
   
   path('store/stripe/', views.StripePaymentView.as_view(), name='stripe_payment'),
   path('store/stripe/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),

   path('store/paypal/create-payment/', views.create_paypal_payment, name='create_paypal_payment'),
   path('store/paypal/execute/',views.execute_paypal_payment, name='execute_paypal_payment'),

   path('payments/success/', views.payment_success, name='create_paypal_payment'),
   path('payments/cancel/',views.payment_cancel, name='execute_paypal_payment'),
]

# handler404 = f"{app_name}.views.page_404"