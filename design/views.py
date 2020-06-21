from django.shortcuts import render
from design.forms import (
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
from django.http import JsonResponse, HttpResponse
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
import json

# Create your views here.


@login_required
def index(request, project_name=""):
    """
        Views for design index
        :param request, project_name if using existing project:
        :return render index_design.html:
    """

    configs = {}
    if request.method == "GET" and project_name != "":
        project = Project.objects.get(
            name=project_name.replace("__", " "), user_id=request.user.id
        )
        roof = Roof.objects.get(project_id=project.id)
        implantation = Implantation.objects.get(roof_id=roof.id)
        configs_queryset = Config.objects.filter(project_id=project.id)
        for config in configs_queryset:
            configs["config" + str(config.index)] = ConfigForm(
                initial={
                    "inverter_id": config.inverter_id.id,
                    "inverter_quantity": config.inverter_quantity,
                    "index": config.index,
                }
            )

            mpps_in_conf = MPP.objects.filter(config_id=config.id)
            for mpp in mpps_in_conf:
                configs[
                    "config" + str(config.index) + "_mpp" + str(mpp.index)
                ] = MPPForm(
                    initial={
                        "serial": mpp.serial,
                        "parallel": mpp.parallel,
                        "index": mpp.index,
                    }
                )

        configs_index = [config.index for config in configs_queryset]
        for config_index in range(1, 4):
            if config_index not in configs_index:
                configs["config" + str(config_index)] = ConfigForm(
                    initial={"index": config_index}
                )
                for mpp_index in range(1, 4):
                    configs[
                        "config"
                        + str(config_index)
                        + "_mpp"
                        + str(mpp_index)
                    ] = MPPForm(initial={"index": mpp_index})
            else:
                mpps_in_conf = MPP.objects.filter(config_id=config.id)
                mpps_index = [mpp.index for mpp in mpps_in_conf]
                for mpp_index in range(1, 4):
                    if mpp_index not in mpps_index:
                        configs[
                            "config"
                            + str(config_index)
                            + "_mpp"
                            + str(mpp_index)
                        ] = MPPForm(initial={"index": mpp_index})

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

        for config_index in range(1, 4):
            for mpp_index in range(1, 4):
                configs["config" + str(config_index)] = ConfigForm(
                    initial={"index": config_index}
                )
                for mpp_index in range(1, 4):
                    configs[
                        "config"
                        + str(config_index)
                        + "_mpp"
                        + str(mpp_index)
                    ] = MPPForm(initial={"index": mpp_index})

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
            "forms_config": configs,
        },
    )


@login_required
def get_localisation_data(request):
    """
        Views to retrieve localisation data from api
        :param request:
        :return JsonResponse with status and localisation if ok:
    """
    if request.method == "POST":
        try:
            search_text = request.POST["search"]
            loc = Localisation(search_text).data
            return JsonResponse({"status": True, "loc": loc})
        except Exception:
            return JsonResponse({"status": False})
    return JsonResponse({"status": False})


@login_required
def add_city(request):
    """
        Views to add city in the database
        :param request:
        :return JsonResponse with status and added city name and id if ok:
    """
    if request.method == "POST":
        try:
            city = CityForm(request.POST)
            if city.is_valid():
                city.save()
                city_added = City.objects.get(name=request.POST["name"])
                return JsonResponse(
                    {
                        "success": True,
                        "name": city_added.name,
                        "id": city_added.id,
                    }
                )
            else:
                return JsonResponse({"errors": city.errors})
        except Exception:  # pragma: no cover
            return JsonResponse({"errors": city.errors})

    return JsonResponse({"errors": True})


@login_required
def add_panel(request):
    """
        Views to add panel to database
        :param request:
        :return JsonResponse with status and panel model and id if ok:
    """
    if request.method == "POST":
        panel = PanelForm(request.POST)
        try:
            if panel.is_valid():
                panel.save()
                panel_added = Panel.objects.get(
                    model=request.POST["model"]
                )
                return JsonResponse(
                    {
                        "success": True,
                        "model": panel_added.model,
                        "id": panel_added.id,
                    }
                )
            else:
                return JsonResponse({"errors": panel.errors})
        except Exception:  # pragma: no cover
            return JsonResponse({"errors": panel.errors})

    return HttpResponse()


@login_required
def add_inverter(request):
    """
        Views to add inverter to database
        :param request:
        :return JsonResponse with status and inverter model and id if ok:
    """
    if request.method == "POST":
        try:
            inverter = InverterForm(request.POST)
            if inverter.is_valid():
                inverter.save()
                inverter_added = Inverter.objects.get(
                    model=request.POST["model"]
                )
                return JsonResponse(
                    {
                        "success": True,
                        "model": inverter_added.model,
                        "id": inverter_added.id,
                    }
                )
            else:
                return JsonResponse({"errors": inverter.errors})
        except Exception:  # pragma: no cover
            return JsonResponse({"errors": inverter.errors})

    return HttpResponse()


@login_required
def valid_project(request):
    """
        Views to validate project form
        :param request:
        :return JsonResponse with status and errors if not ok:
    """
    if request.method == "POST":
        project = ProjectForm(request.POST)
        try:
            if project.is_valid():
                request.session["panel_id"] = project.cleaned_data[
                    "panel_id"
                ].id
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": project.errors})
        except Exception:
            return JsonResponse({"errors": project.errors})


@login_required
def save_project(request):
    """
        Views to save project form
        :param request:
        :return JsonResponse with status and errors if not ok:
    """
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
        except Exception:
            return JsonResponse({"errors": project.errors})


@login_required
def valid_roof(request):
    """
        Views to validate roof form
        :param request:
        :return JsonResponse with status and errors if not ok:
    """
    if request.method == "POST":
        try:
            roof = RoofForm(
                request.POST,
                panel=Panel.objects.get(id=request.session["panel_id"]),
            )
            if roof.is_valid():
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": roof.errors})
        except Exception:
            return JsonResponse({"errors": roof.errors})


@login_required
def save_roof(request):
    """
        Views to save roof form
        :param request:
        :return JsonResponse with status and errors if not ok:
    """
    if request.method == "POST":
        roof = RoofForm(
            request.POST,
            panel=Panel.objects.get(id=request.session["panel_id"]),
        )
        try:
            if roof.is_valid() and request.session["project_id"]:
                roof = roof.save(commit=False)
                project = Project.objects.get(
                    id=request.session["project_id"]
                )
                roof.project_id = project
                roof.save()
                saved_roof = Roof.objects.get(project_id=project.id)
                request.session["roof_id"] = saved_roof.id
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": roof.errors})
        except Exception:
            return JsonResponse({"errors": roof.errors})


@login_required
def valid_implantation(request):
    """
        Views to validate implantation form
        :param request:
        :return JsonResponse with status and errors if not ok:
    """
    if request.method == "POST":
        implantation = ImplantationForm(request.POST)
        try:
            if implantation.is_valid():
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": implantation.errors})
        except Exception:
            return JsonResponse({"errors": implantation.errors})


@login_required
def save_implantation(request):
    """
        Views to save implantation form
        :param request:
        :return JsonResponse with status and errors if not ok:
    """
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
        except Exception:
            return JsonResponse({"errors": implantation.errors})


@login_required
def valid_configuration(request):
    """
        Views to validate configuration form
        :param request:
        :return JsonResponse with status and errors if not ok:
    """
    if request.method == "POST":
        configuration = ConfigForm(request.POST)
        try:
            if configuration.is_valid():
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": configuration.errors})
        except Exception:
            return JsonResponse({"errors": configuration.errors})


@login_required
def save_configuration(request):
    """
        Views to save configuration form
        :param request:
        :return JsonResponse with status and errors if not ok:
    """
    if request.method == "POST":
        configuration = ConfigForm(request.POST)
        try:
            if configuration.is_valid():
                configuration = configuration.save(commit=False)
                project = Project.objects.get(
                    id=request.session["project_id"]
                )
                configuration.project_id = project
                configuration.save()
                saved_config = Config.objects.get(
                    project_id=project.id, index=configuration.index
                )
                request.session["config_id"] = saved_config.id
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": configuration.errors})
        except Exception:
            return JsonResponse({"errors": configuration.errors})


@login_required
def valid_mpp(request):
    """
        Views to validate mpp form
        :param request:
        :return JsonResponse with status and errors if not ok:
    """
    if request.method == "POST":
        mpp = MPPForm(request.POST)
        try:
            if mpp.is_valid():
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": mpp.errors})
        except Exception:
            return JsonResponse({"errors": mpp.errors})


@login_required
def save_mpp(request):
    """
        Views to save mpp form
        :param request:
        :return JsonResponse with status and errors if not ok:
    """
    if request.method == "POST":
        mpp = MPPForm(request.POST)
        try:
            if mpp.is_valid():
                mpp = mpp.save(commit=False)
                config = Config.objects.get(
                    id=request.session["config_id"]
                )
                mpp.config_id = config
                mpp.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"errors": mpp.errors})
        except Exception:
            return JsonResponse({"errors": mpp.errors})


@login_required
def calcul_implantation(request):
    """
        Views to calculate implantation data
        :param request:
        :return JsonResponse with status and implantation values if ok:
    """
    if request.method == "POST":
        data = request.POST
        try:
            implantation = Implantation_calculation(data)
            return JsonResponse(
                {"success": True, "implantation_values": implantation.data}
            )
        except Exception:
            return JsonResponse({"errors": True})


@login_required
def calcul_configuration(request):
    """
        Views to calculate configuration data
        :param request:
        :return JsonResponse with status and configuration values if ok:
    """
    if request.method == "POST":
        data = json.loads(request.POST.get("data", ""))
        try:
            configuration = Calculation(data)
            return JsonResponse(
                {
                    "success": True,
                    "configuration_values": configuration.data,
                }
            )
        except Exception:
            return JsonResponse({"errors": True})


@login_required
def inverter_data(request):
    """
        Views to retrieve inverter data
        :param request:
        :return JsonResponse with status and inverter datas if ok:
    """
    data = request.POST
    if request.method == "POST":
        try:
            inverter = Inverter.objects.get(id=int(data["inverter_id"]))
            return JsonResponse(
                {
                    "success": True,
                    "data": serializers.serialize("json", [inverter]),
                }
            )
        except Exception:
            return JsonResponse({"errors": True})


@login_required
def production_data(request):
    """
        Views to retrieve production datas from models and calculation
        :param request:
        :return JsonResponse with status and informations values if ok:
    """
    if request.method == "POST":
        data = json.loads(request.POST.get("data", ""))
        try:
            information = Informations()
            infos = information.get_production_information(data)
            return JsonResponse({"success": True, "infos": infos})
        except Exception:
            return JsonResponse({"errors": True})


@login_required
def calculate_production(request):
    """
        Views to calculate production datas
        :param request:
        :return JsonResponse with status and production values if ok:
    """
    if request.method == "POST":
        data = json.loads(request.POST.get("data", ""))
        try:
            datas = Production(data).datas
            return JsonResponse({"success": True, "datas": datas})
        except Exception:
            return JsonResponse({"errors": True})
