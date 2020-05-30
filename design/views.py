from django.shortcuts import render
from .forms import ProjectForm, CityForm, PanelForm, RoofForm, ImplantationForm
from django.contrib.auth.decorators import login_required
from design.api import TemperatureData, IrradianceData, Localisation
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from project.models import City
from design.models import Panel, Temperature_coefficient
from design.implantation_calculation import Implantation_calculation
import json

# Create your views here.


@login_required
def index(request):
    """
    Views for home
    :param request:
    :return render home.html:
    """
    if request.method == "POST":
        project = ProjectForm(data=request.POST)
        try:
            if project.is_valid():
                project.save(commit=False)
                project.user_id = request.user
                project.save()
        except:
            pass
    else:
        project = ProjectForm()
        city = CityForm()
        panel = PanelForm()
        roof = RoofForm()
        implantation = ImplantationForm()

    return render(
        request,
        "index.html",
        {
            "form_project": project,
            "form_city": city,
            "form_panel": panel,
            "form_roof": roof,
            "form_implantation": implantation,
        },
    )


@login_required
def get_meteo_data(request):
    if request.method == "POST":
        search_text = request.POST["search"]
        try:
            localisation = Localisation(search_text)
            return JsonResponse({"status": True, "localisation": localisation.data,})
        except Exception as E:
            return JsonResponse({"status": False})
    return JsonResponse({"status": False})


@login_required
def add_city(request):
    if request.method == "POST":
        city = CityForm(request.POST)
        try:
            if city.is_valid():
                city.save()
                city_added = City.objects.get(name=request.POST["name"])
                messages.success(request, "La ville a été créée")
                return JsonResponse(
                    {"success": True, "name": city_added.name, "id": city_added.id}
                )
            else:
                response = [v for k, v in city.errors.items()]
                return JsonResponse({"errors": response})
        except Exception as E:  # pragma: no cover
            messages.warning(request, "Erreur lors de l'enregistrement de la ville")
            return JsonResponse()

    return HttpResponse()


@login_required
def add_panel(request):
    if request.method == "POST":
        panel = PanelForm(request.POST)
        try:
            if panel.is_valid():
                panel.save()
                panel_added = Panel.objects.get(model=request.POST["model"])
                messages.success(request, "Le panneau a été créé")
                return JsonResponse(
                    {"success": True, "model": panel_added.model, "id": panel_added.id}
                )
            else:
                response = [v for k, v in panel.errors.items()]
                return JsonResponse({"errors": response})
        except Exception as E:  # pragma: no cover
            messages.warning(request, "Erreur lors de l'enregistrement du panneau")
            return JsonResponse()

    return HttpResponse()


@login_required
def save_roof(request):
    pass


@login_required
def valid_project(request):
    if request.method == "POST":
        project = ProjectForm(request.POST)
        try:
            if project.is_valid():
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": project.errors})
        except:
            return JsonResponse({"errors": True})


@login_required
def valid_roof(request):
    if request.method == "POST":
        roof = RoofForm(request.POST)
        try:
            if roof.is_valid():
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": roof.errors})
        except Exception as E:
            return JsonResponse({"errors": True})


@login_required
def valid_implantation(request):
    if request.method == "POST":
        implantation = ImplantationForm(request.POST)
        try:
            if implantation.is_valid():
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": implantation.errors})
        except Exception as E:
            return JsonResponse({"errors": True})


@login_required
def calcul_implantation(request):
    if request.method == "POST":
        data = request.POST
        try:
            implantation = Implantation_calculation(data)
            return JsonResponse(
                    {"success": True, "implantation_values": implantation.data}
            )
        except Exception as E:
            return JsonResponse({"errors": True})
