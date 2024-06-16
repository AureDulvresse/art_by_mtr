from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("", views.show, name="myAccount"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout"),
    path("register", views.register_page, name="register"),
    path("update-account", views.update, name="update-account"),
    path("delete-account", views.destroy, name="delete-account"),
]