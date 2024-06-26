from django.contrib.auth import views as auth_views
from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("", views.show, name="profile"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout"),
    path("register", views.register_page, name="register"),
    path("update-account", views.update, name="update-account"),
    path('change-password/', views.change_password, name='change-password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path("delete-account", views.destroy, name="delete-account"),
]