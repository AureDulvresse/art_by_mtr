from django.urls import path
# from django.conf.urls import handler404

from store import views

app_name = "blog"

urlpatterns = [
   path('', views.gallery_page, name="artwork-list"),
   path('artwork/:pk', views.artwork_detail_page)
]

# handler404 = f"{app_name}.views.page_404"