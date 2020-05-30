"""Contains the application’s url."""
from django.urls import path
from . import views

app_name = "design"

urlpatterns = [
    path("design/", views.index, name="index"),
    path("get_meteo_data/", views.get_meteo_data, name="get_meteo_data",),
    path("add_city/", views.add_city, name="add_city"),
    path("add_panel/", views.add_panel, name="add_panel"),
    path("save_roof/", views.save_roof, name="save_roof"),
    path("valid_project/", views.valid_project, name="valid_project"),
    path("valid_roof/", views.valid_roof, name="valid_roof"),
    path("valid_implantation/", views.valid_implantation, name="valid_implantation"),
    path("calcul_implantation/", views.calcul_implantation, name="calcul_implantation"),
]
