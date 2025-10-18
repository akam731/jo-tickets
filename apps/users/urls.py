"""Routage de l’application."""

from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("inscription/", views.signup_view, name="signup"),
    path("connexion/", views.login_view, name="login"),
    path("profil/", views.profile_view, name="profile"),
    path("deconnexion/", views.logout_view, name="logout"),
]


