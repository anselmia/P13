"""Contains the application’s url."""
from django.urls import path
from . import views

app_name = "design"

urlpatterns = [
    path("design/", views.index, name="index"),
]
