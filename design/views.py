from django.shortcuts import render
from .forms import (
    ProjectForm,
    CityForm,
    PanelForm,
    RoofForm,
    ImplantationForm,
    ConfigForm,
    MPPForm,
    InverterForm,
)
from django.contrib.auth.decorators import login_required
from design.api import Localisation
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from design.models import (
    Panel,
    Inverter,
    Roof,
    Config,
    Implantation,
    City,
    Project,
    MPP,
)
from design.implantation_calculation import Implantation_calculation
from design.configuration_calculation import Calculation
from design.energy_calculation import Production
from .informations import Informations
from django.core import serializers
from django.forms import formset_factory
import json

# Create your views here.


@login_required
def index(request, project_name=""):
    """
    Views for home
    :param request:
    :return render home.html:
    """
    config1 = None
    config2 = None
    config3 = None
    mpp11 = None
    mpp12 = None
    mpp13 = None
    mpp21 = None
    mpp22 = None
    mpp23 = None
    mpp31 = None
    mpp32 = None
    mpp33 = None

    if request.method == "GET" and project_name != "":
        project = Project.objects.get(name=project_name, user_id=request.user.id)
        roof = Roof.objects.get(project_id=project.id)
        implantation = Implantation.objects.get(roof_id=roof.id)
        configs = Config.objects.filter(project_id=project.id)
        for config in configs:
            if config.index == 1:
                config1 = ConfigForm(
                    initial={
                        "inverter_id": config.inverter_id.id,
                        "inverter_quantity": config.inverter_quantity,
                        "index": config.index,
                    }
                )
                mpps_in_conf = MPP.objects.filter(config_id=config.id)
                for mpp in mpps_in_conf:
                    if mpp.index == 1:
                        mpp11 = MPPForm(
                            initial={
                                "serial": mpp.serial,
                                "parallel": mpp.parallel,
                                "index": 1,
                            }
                        )
                    elif mpp.index == 2:
                        mpp12 = MPPForm(
                            initial={
                                "serial": mpp.serial,
                                "parallel": mpp.parallel,
                                "index": 2,
                            }
                        )
                    elif mpp.index == 3:
                        mpp13 = MPPForm(
                            initial={
                                "serial": mpp.serial,
                                "parallel": mpp.parallel,
                                "index": 3,
                            }
                        )

            elif config.index == 2:
                config2 = ConfigForm(
                    initial={
                        "inverter_id": config.inverter_id.id,
                        "inverter_quantity": config.inverter_quantity,
                        "index": config.index,
                    }
                )
                mpps_in_conf = MPP.objects.filter(config_id=config.id)
                for mpp in mpps_in_conf:
                    if mpp.index == 1:
                        mpp21 = MPPForm(
                            initial={
                                "serial": mpp.serial,
                                "parallel": mpp.parallel,
                                "index": 1,
                            }
                        )
                    elif mpp.index == 2:
                        mpp22 = MPPForm(
                            initial={
                                "serial": mpp.serial,
                                "parallel": mpp.parallel,
                                "index": 2,
                            }
                        )
                    elif mpp.index == 3:
                        mpp23 = MPPForm(
                            initial={
                                "serial": mpp.serial,
                                "parallel": mpp.parallel,
                                "index": 3,
                            }
                        )

            elif config.index == 3:
                config3 = ConfigForm(
                    initial={
                        "inverter_id": config.inverter_id.id,
                        "inverter_quantity": config.inverter_quantity,
                        "index": config.index,
                    }
                )
                mpps_in_conf = MPP.objects.filter(config_id=config.id)
                for mpp in mpps_in_conf:
                    if mpp.index == 1:
                        mpp31 = MPPForm(
                            initial={
                                "serial": mpp.serial,
                                "parallel": mpp.parallel,
                                "index": 1,
                            }
                        )
                    elif mpp.index == 2:
                        mpp32 = MPPForm(
                            initial={
                                "serial": mpp.serial,
                                "parallel": mpp.parallel,
                                "index": 2,
                            }
                        )
                    elif mpp.index == 3:
                        mpp33 = MPPForm(
                            initial={
                                "serial": mpp.serial,
                                "parallel": mpp.parallel,
                                "index": 3,
                            }
                        )

        if config1 == None:
            config1 = ConfigForm()
        if config2 == None:
            config2 = ConfigForm()
        if config3 == None:
            config3 = ConfigForm()
        if mpp11 == None:
            mpp11 = MPPForm()
        if mpp12 == None:
            mpp12 = MPPForm()
        if mpp13 == None:
            mpp13 = MPPForm()
        if mpp21 == None:
            mpp21 = MPPForm()
        if mpp22 == None:
            mpp22 = MPPForm()
        if mpp23 == None:
            mpp23 = MPPForm()
        if mpp31 == None:
            mpp31 = MPPForm()
        if mpp32 == None:
            mpp32 = MPPForm()
        if mpp33 == None:
            mpp33 = MPPForm()

        project = ProjectForm(
            initial={
                "name": project.name,
                "city_id": project.city_id.id,
                "panel_id": project.panel_id.id,
                "user_id": project.user_id.id,
            }
        )
        roof = RoofForm(
            initial={
                "roof_type_id": roof.roof_type_id.id,
                "top_length": roof.top_length,
                "bottom_length": roof.bottom_length,
                "width": roof.width,
                "height": roof.height,
                "orientation": roof.orientation,
                "tilt": roof.tilt,
            }
        )
        implantation = ImplantationForm(
            initial={
                "panel_orientation": implantation.panel_orientation.id,
                "panel_implantation": implantation.panel_implantation.id,
                "vertical_overlapping": implantation.vertical_overlapping,
                "horizontal_overlapping": implantation.horizontal_overlapping,
                "vertical_spacing": implantation.vertical_spacing,
                "horizontal_spacing": implantation.horizontal_spacing,
                "distance_top": implantation.distance_top,
                "distance_bottom": implantation.distance_bottom,
                "distance_left": implantation.distance_left,
                "distance_right": implantation.distance_right,
                "abergement_top": implantation.abergement_top,
                "abergement_bottom": implantation.abergement_bottom,
                "abergement_left": implantation.abergement_left,
                "abergement_right": implantation.abergement_right,
            }
        )

    else:
        project = ProjectForm()
        roof = RoofForm()
        implantation = ImplantationForm()
        config1 = ConfigForm(initial={"index": 1,})
        config2 = ConfigForm(initial={"index": 2,})
        config3 = ConfigForm(initial={"index": 3,})
        mpp11 = MPPForm(initial={"index": 1,})
        mpp12 = MPPForm(initial={"index": 2,})
        mpp13 = MPPForm(initial={"index": 3,})
        mpp21 = MPPForm(initial={"index": 1,})
        mpp22 = MPPForm(initial={"index": 2,})
        mpp23 = MPPForm(initial={"index": 3,})
        mpp31 = MPPForm(initial={"index": 1,})
        mpp32 = MPPForm(initial={"index": 2,})
        mpp33 = MPPForm(initial={"index": 3,})

    city = CityForm()
    panel = PanelForm()
    inverter = InverterForm()

    return render(
        request,
        "index_design.html",
        {
            "form_project": project,
            "form_city": city,
            "form_panel": panel,
            "form_inverter": inverter,
            "form_roof": roof,
            "form_implantation": implantation,
            "form_config1": config1,
            "form_config2": config2,
            "form_config3": config3,
            "form_mpp11": mpp11,
            "form_mpp12": mpp12,
            "form_mpp13": mpp13,
            "form_mpp21": mpp21,
            "form_mpp22": mpp22,
            "form_mpp23": mpp23,
            "form_mpp31": mpp31,
            "form_mpp32": mpp32,
            "form_mpp33": mpp33,
        },
    )


@login_required
def get_localisation_data(request):
    if request.method == "POST":
        search_text = request.POST["search"]
        try:
            loc = Localisation(search_text).data
            return JsonResponse({"status": True, "loc": loc,})
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
                return JsonResponse({"errors": city.errors})
        except Exception as E:  # pragma: no cover
            return JsonResponse({"errors": city.errors})

    return HttpResponse()


@login_required
def add_panel(request):
    if request.method == "POST":
        panel = PanelForm(request.POST)
        try:
            if panel.is_valid():
                panel.save()
                panel_added = Panel.objects.get(model=request.POST["model"])
                return JsonResponse(
                    {"success": True, "model": panel_added.model, "id": panel_added.id}
                )
            else:
                return JsonResponse({"errors": panel.errors})
        except Exception as E:  # pragma: no cover
            return JsonResponse({"errors": panel.errors})

    return HttpResponse()


@login_required
def add_inverter(request):
    if request.method == "POST":
        inverter = InverterForm(request.POST)
        try:
            if inverter.is_valid():
                inverter.save()
                inverter_added = Inverter.objects.get(model=request.POST["model"])
                return JsonResponse(
                    {
                        "success": True,
                        "model": inverter_added.model,
                        "id": inverter_added.id,
                    }
                )
            else:
                return JsonResponse({"errors": inverter_added.errors})
        except Exception as E:  # pragma: no cover
            return JsonResponse({"errors": inverter_added.errors})

    return HttpResponse()


@login_required
def valid_project(request):
    if request.method == "POST":
        project = ProjectForm(request.POST)
        try:
            if project.is_valid():
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": project.errors})
        except Exception as e:
            return JsonResponse({"errors": project.errors})


@login_required
def save_project(request):
    if request.method == "POST":
        project = ProjectForm(request.POST)
        try:
            if project.is_valid():
                project = project.save(commit=False)
                project.user_id = request.user
                project.save()
                saved_project = Project.objects.get(
                    name=project.name, user_id=request.user
                )
                request.session["project_id"] = saved_project.id
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": project.errors})
        except Exception as e:
            return JsonResponse({"errors": project.errors})


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
            return JsonResponse({"errors": roof.errors})


@login_required
def save_roof(request):
    if request.method == "POST":
        roof = RoofForm(request.POST)
        try:
            if roof.is_valid() and request.session["project_id"]:
                roof = roof.save(commit=False)
                project = Project.objects.get(id=request.session["project_id"])
                roof.project_id = project
                roof.save()
                saved_roof = Roof.objects.get(project_id=project.id)
                request.session["roof_id"] = saved_roof.id
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": roof.errors})
        except Exception as E:
            return JsonResponse({"errors": roof.errors})


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
            return JsonResponse({"errors": implantation.errors})


@login_required
def save_implantation(request):
    if request.method == "POST":
        implantation = ImplantationForm(request.POST)
        try:
            if implantation.is_valid():
                implantation = implantation.save(commit=False)
                roof_id = request.session["roof_id"]
                roof = Roof.objects.get(id=roof_id)
                implantation.roof_id = roof
                implantation.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": implantation.errors})
        except Exception as E:
            return JsonResponse({"errors": implantation.errors})


@login_required
def valid_configuration(request):
    if request.method == "POST":
        configuration = ConfigForm(request.POST)
        try:
            if configuration.is_valid():
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": configuration.errors})
        except Exception as E:
            return JsonResponse({"errors": configuration.errors})


@login_required
def save_configuration(request):
    if request.method == "POST":
        configuration = ConfigForm(request.POST)
        try:
            if configuration.is_valid():
                configuration = configuration.save(commit=False)
                project = Project.objects.get(id=request.session["project_id"])
                configuration.project_id = project
                configuration.save()
                saved_config = Config.objects.get(
                    project_id=project.id, index=configuration.index
                )
                request.session["config_id"] = saved_config.id
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": configuration.errors})
        except Exception as E:
            return JsonResponse({"errors": configuration.errors})


@login_required
def valid_mpp(request):
    if request.method == "POST":
        mpp = MPPForm(request.POST)
        try:
            if mpp.is_valid():
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": mpp.errors})
        except Exception as E:
            return JsonResponse({"errors": mpp.errors})


@login_required
def save_mpp(request):
    if request.method == "POST":
        mpp = MPPForm(request.POST)
        try:
            if mpp.is_valid():
                mpp = mpp.save(commit=False)
                config = Config.objects.get(id=request.session["config_id"])
                mpp.config_id = config
                mpp.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": mpp.errors})
        except Exception as E:
            return JsonResponse({"errors": mpp.errors})


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


@login_required
def calcul_configuration(request):
    if request.method == "POST":
        data = json.loads(request.POST.get("data", ""))
        try:
            configuration = Calculation(data)
            return JsonResponse(
                {"success": True, "configuration_values": configuration.data}
            )
        except Exception as E:
            return JsonResponse({"errors": True})


@login_required
def inverter_data(request):
    data = request.POST
    if request.method == "POST":
        try:
            inverter = Inverter.objects.get(id=int(data["inverter_id"]))
            return JsonResponse(
                {"success": True, "data": serializers.serialize("json", [inverter,]),}
            )
        except Exception as E:
            return JsonResponse({"errors": True})


@login_required
def production_data(request):
    if request.method == "POST":
        data = json.loads(request.POST.get("data", ""))
        try:
            information = Informations()
            infos = information.get_production_information(data)
            return JsonResponse({"success": True, "infos": infos})
        except Exception as E:
            return JsonResponse({"errors": True})


@login_required
def calculate_production(request):
    if request.method == "POST":
        data = json.loads(request.POST.get("data", ""))
        try:
            datas = Production(data).datas
            return JsonResponse({"success": True, "datas": datas})
        except Exception as E:
            return JsonResponse({"errors": True})
