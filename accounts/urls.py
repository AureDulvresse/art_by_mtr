from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("", views.UserController.show, name="myAccount"),
    path("login", views.AuthController.login_page, name="login"),
    path("logout", views.AuthController.logout_page, name="logout"),
    path("register", views.AuthController.register_page, name="register"),
    path("update-account", views.UserController.update, name="update-account"),
    path("delete-account", views.UserController.destroy, name="delete-account"),
]