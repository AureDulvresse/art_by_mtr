from django.urls import path
# from django.conf.urls import handler404

from blog import views

app_name = "blog"

urlpatterns = [
   path('', views.blog_page, name="index"),
   path('post/:slug', views.post_detail_page, name="post-detail"),
]

# handler404 = f"{app_name}.views.page_404"