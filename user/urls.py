from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("user_dashboard/", views.user_dashboard, name="user_dashboard"),
    path("update/", views.update_profile, name="update_profile"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin_logout/", views.admin_logout, name="admin_logout"),
    path("user_login/", views.user_login, name="user_login"),  
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
]