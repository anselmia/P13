"""Contains the application’s url."""
from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.home, name="index"),
    path("mentions/", views.mentions, name="mentions"),
]
