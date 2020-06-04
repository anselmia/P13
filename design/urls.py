"""Contains the application’s url."""
from django.urls import path
from . import views

app_name = "design"

urlpatterns = [
    path("design/", views.index, name="index"),
    path(
        "get_localisation_data/",
        views.get_localisation_data,
        name="get_localisation_data",
    ),
    path("add_city/", views.add_city, name="add_city"),
    path("add_panel/", views.add_panel, name="add_panel"),
    path("save_roof/", views.save_roof, name="save_roof"),
    path("valid_project/", views.valid_project, name="valid_project"),
    path("valid_roof/", views.valid_roof, name="valid_roof"),
    path("valid_implantation/", views.valid_implantation, name="valid_implantation"),
    path("calcul_implantation/", views.calcul_implantation, name="calcul_implantation"),
    path("valid_configuration/", views.valid_configuration, name="valid_configuration"),
    path("valid_mpp/", views.valid_mpp, name="valid_mpp"),
    path("save_project/", views.save_project, name="save_project"),
    path("save_roof/", views.save_roof, name="save_roof"),
    path("save_implantation/", views.save_implantation, name="save_implantation"),
    path("calcul_implantation/", views.calcul_implantation, name="calcul_implantation"),
    path("save_configuration/", views.save_configuration, name="save_configuration"),
    path("save_mpp/", views.save_mpp, name="save_mpp"),
    path(
        "calcul_configuration/", views.calcul_configuration, name="calcul_configuration"
    ),
    path("inverter_data/", views.inverter_data, name="inverter_data"),
    path("production_data/", views.production_data, name="production_data"),
    path(
        "calculate_production/", views.calculate_production, name="calculate_production"
    ),
]
