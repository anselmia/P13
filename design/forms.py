from django import forms
from project.models import City, Project
from .models import (
    Panel,
    Technology,
    Manufacturer,
    Temperature_coefficient,
    Roof,
    Roof_type,
    Implantation,
    Orientation,
    Pose,
    Config,
    MPP,
    Inverter,
)
from user.models import User
from django.forms import ModelForm
import math


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ("name", "city_id", "panel_id")

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update(
            {"value": 0, "class": "container_100 cn"}
        )
        self.fields["name"].required = True

    city_id = forms.ModelChoiceField(
        queryset=City.objects.all(), label="Ville", required=True, initial=1,
    )
    city_id.widget.attrs["class"] = "round_input container_100 cn"
    panel_id = forms.ModelChoiceField(
        queryset=Panel.objects.all(),
        label="Type de panneaux",
        required=True,
        initial=1,
    )
    panel_id.widget.attrs["class"] = "round_input container_100 cn"


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = (
            "name",
            "lat",
            "lon",
        )

    def __init__(self, *args, **kwargs):
        super(CityForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "find_city", "readonly": True}
        )
        self.fields["name"].required = True
        self.fields["lat"].widget.attrs.update({"class": "find_lat", "readonly": True})
        self.fields["lat"].required = True
        self.fields["lon"].widget.attrs.update({"class": "find_lon", "readonly": True})
        self.fields["lon"].required = True


class PanelForm(ModelForm):
    class Meta:
        model = Panel
        fields = (
            "model",
            "manufacturer_id",
            "technology_id",
            "power",
            "tolerance",
            "radiation",
            "temperature",
            "short_circuit_current",
            "open_circuit_voltage",
            "temperature_factor_current",
            "temperature_factor_voltage",
            "temperature_factor_power",
            "temperature_factor_current_type",
            "temperature_factor_voltage_type",
            "temperature_factor_power_type",
            "mpp_current",
            "mpp_voltage",
            "voltage_max",
            "length",
            "width",
            "serial_cell_quantity",
            "parallel_cell_quantity",
            "cell_surface",
            "comment",
        )

    def __init__(self, *args, **kwargs):
        super(PanelForm, self).__init__(*args, **kwargs)
        self.fields["model"].required = True
        self.fields["power"].required = True
        self.fields["tolerance"].required = True
        self.fields["radiation"].required = True
        self.fields["temperature"].required = True
        self.fields["short_circuit_current"].required = True
        self.fields["open_circuit_voltage"].required = True
        self.fields["temperature_factor_current"].required = True
        self.fields["temperature_factor_voltage"].required = True
        self.fields["temperature_factor_power"].required = True
        self.fields["mpp_current"].required = True
        self.fields["mpp_voltage"].required = True
        self.fields["voltage_max"].required = True
        self.fields["length"].required = True
        self.fields["width"].required = True
        self.fields["serial_cell_quantity"].required = True
        self.fields["parallel_cell_quantity"].required = True
        self.fields["cell_surface"].required = True
        self.fields["cell_surface"].required = False

    technology_id = forms.ModelChoiceField(
        queryset=Technology.objects.all(), label="Technologie", required=True
    )
    technology_id.widget.attrs["class"] = "round_input container_100"
    manufacturer_id = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(), label="Fabricant", required=True
    )
    manufacturer_id.widget.attrs["class"] = "round_input container_100"
    temperature_factor_current_type = forms.ModelChoiceField(
        queryset=Temperature_coefficient.objects.all(), label="", required=True
    )
    temperature_factor_current_type.widget.attrs["class"] = "round_input container_100"
    temperature_factor_voltage_type = forms.ModelChoiceField(
        queryset=Temperature_coefficient.objects.all(), label="", required=True
    )
    temperature_factor_voltage_type.widget.attrs["class"] = "round_input container_100"
    temperature_factor_power_type = forms.ModelChoiceField(
        queryset=Temperature_coefficient.objects.all(), label="", required=True
    )
    temperature_factor_power_type.widget.attrs["class"] = "round_input container_100"


class RoofForm(ModelForm):
    class Meta:
        model = Roof
        fields = (
            "roof_type",
            "bottom_length",
            "top_length",
            "width",
            "height",
            "orientation",
            "tilt",
        )

    def __init__(self, *args, **kwargs):
        super(RoofForm, self).__init__(*args, **kwargs)
        self.fields["bottom_length"].required = True
        self.fields["bottom_length"].widget.attrs.update({"value": 41})
        self.fields["top_length"].required = False
        self.fields["top_length"].widget.attrs.update({"value": 0})
        self.fields["height"].required = False
        self.fields["height"].widget.attrs.update({"value": 0})
        self.fields["width"].required = False
        self.fields["width"].widget.attrs.update({"value": 5})
        self.fields["orientation"].required = True
        self.fields["orientation"].widget.attrs.update({"value": 0})
        self.fields["tilt"].required = True
        self.fields["tilt"].widget.attrs.update({"value": 0})
        self.fields["bottom_length"].widget.attrs.update(
            {"class": "container_100 round_input"}
        )
        self.fields["top_length"].widget.attrs.update(
            {"class": "container_100 round_input"}
        )
        self.fields["width"].widget.attrs.update({"class": "container_100 round_input"})
        self.fields["height"].widget.attrs.update(
            {"class": "container_100 round_input"}
        )
        self.fields["orientation"].widget.attrs.update(
            {"class": "container_100 round_input"}
        )
        self.fields["tilt"].widget.attrs.update({"class": "container_100 round_input "})

    roof_type = forms.ModelChoiceField(
        queryset=Roof_type.objects.all(),
        label="Type de toîture",
        required=True,
        initial=1,
    )
    roof_type.widget.attrs["class"] = "round_input container_100"

    def clean(self):
        # data from the form is fetched using super function
        super(RoofForm, self).clean()

        roof_type = self.cleaned_data.get("roof_type")
        bottom_length = self.cleaned_data.get("bottom_length")
        top_length = self.cleaned_data.get("top_length")
        width = self.cleaned_data.get("width")
        height = self.cleaned_data.get("height")

        if roof_type is not None:
            if roof_type.id == 1 or roof_type.id == 3:
                if bottom_length is None or bottom_length == "" or bottom_length <= 0:
                    self._errors["bottom_length"] = self.error_class(
                        ["Veuillez vérifier la valeur"]
                    )
                if width is None or width == "" or width <= 0:
                    self._errors["width"] = self.error_class(
                        ["Veuillez vérifier la valeur"]
                    )
                if roof_type.id == 3:
                    if not (
                        bottom_length is None
                        or bottom_length == ""
                        or bottom_length <= 0
                        or width is None
                        or width == ""
                        or width <= 0
                    ):
                        try:
                            height = math.sqrt(
                                (width * width)
                                - ((bottom_length / 2) * (bottom_length / 2))
                            )
                        except:
                            self._errors["bottom_length"] = self.error_class(
                                ["Veuillez vérifier la valeur"]
                            )
                            self._errors["width"] = self.error_class(
                                ["Veuillez vérifier la valeur"]
                            )
            elif roof_type.id == 2:
                if bottom_length is None or bottom_length == "" or bottom_length <= 0:
                    self._errors["bottom_length"] = self.error_class(
                        ["Veuillez vérifier la valeur"]
                    )
                if top_length is None or top_length == "" or top_length <= 0:
                    self._errors["top_length"] = self.error_class(
                        ["Veuillez vérifier la valeur"]
                    )
                if height is None or height == "" or height <= 0:
                    self._errors["height"] = self.error_class(
                        ["Veuillez vérifier la valeur"]
                    )

                if not (
                    bottom_length is None
                    or bottom_length == ""
                    or bottom_length <= 0
                    or top_length is None
                    or top_length == ""
                    or top_length <= 0
                ):
                    if bottom_length < top_length:
                        self._errors["bottom_length"] = self.error_class(
                            ["Veuillez vérifier la valeur"]
                        )
                        self._errors["top_length"] = self.error_class(
                            ["Veuillez vérifier la valeur"]
                        )
        # return any errors if found
        return self.cleaned_data


class ImplantationForm(ModelForm):
    class Meta:
        model = Implantation
        fields = (
            "panel_orientation",
            "panel_implantation",
            "vertical_overlapping",
            "horizontal_overlapping",
            "vertical_spacing",
            "horizontal_spacing",
            "distance_top",
            "distance_bottom",
            "distance_left",
            "distance_right",
            "abergement_top",
            "abergement_bottom",
            "abergement_left",
            "abergement_right",
        )

    def __init__(self, *args, **kwargs):
        super(ImplantationForm, self).__init__(*args, **kwargs)
        self.fields["vertical_overlapping"].required = False
        self.fields["vertical_overlapping"].widget.attrs.update(
            {"value": 0, "class": "cn"}
        )
        self.fields["horizontal_overlapping"].required = False
        self.fields["horizontal_overlapping"].widget.attrs.update(
            {"value": 0, "class": "cn"}
        )
        self.fields["vertical_spacing"].required = False
        self.fields["vertical_spacing"].widget.attrs.update({"value": 0, "class": "cn"})
        self.fields["horizontal_spacing"].required = False
        self.fields["horizontal_spacing"].widget.attrs.update(
            {"value": 0, "class": "cn"}
        )
        self.fields["distance_top"].required = True
        self.fields["distance_top"].widget.attrs.update({"value": 0, "class": "cn"})
        self.fields["distance_bottom"].required = True
        self.fields["distance_bottom"].widget.attrs.update({"value": 0, "class": "cn"})
        self.fields["distance_left"].required = True
        self.fields["distance_left"].widget.attrs.update({"value": 0, "class": "cn"})
        self.fields["distance_right"].required = True
        self.fields["distance_right"].widget.attrs.update({"value": 0, "class": "cn"})
        self.fields["abergement_top"].required = True
        self.fields["abergement_top"].widget.attrs.update({"value": 0, "class": "cn"})
        self.fields["abergement_bottom"].required = True
        self.fields["abergement_bottom"].widget.attrs.update(
            {"value": 0, "class": "cn"}
        )
        self.fields["abergement_left"].required = True
        self.fields["abergement_left"].widget.attrs.update({"value": 0, "class": "cn"})
        self.fields["abergement_right"].required = True
        self.fields["abergement_right"].widget.attrs.update({"value": 0, "class": "cn"})

        self.fields["panel_orientation"].widget.attrs.update(
            {"class": "container_100 round_input cn"}
        )
        self.fields["panel_implantation"].widget.attrs.update(
            {"class": "container_100 round_input cn"}
        )

    panel_orientation = forms.ModelChoiceField(
        queryset=Orientation.objects.all(),
        label="Orientation",
        required=True,
        initial=1,
    )
    panel_implantation = forms.ModelChoiceField(
        queryset=Pose.objects.all(), label="Pose", required=True, initial=1,
    )

    def clean(self):
        # data from the form is fetched using super function
        super(ImplantationForm, self).clean()

        vertical_overlapping = self.cleaned_data.get("vertical_overlapping")
        horizontal_overlapping = self.cleaned_data.get("horizontal_overlapping")
        vertical_spacing = self.cleaned_data.get("vertical_spacing")
        horizontal_spacing = self.cleaned_data.get("horizontal_spacing")
        panel_implantation = self.cleaned_data.get("panel_implantation")

        if panel_implantation is not None:
            if panel_implantation.id == 2:
                if (
                    vertical_spacing is None
                    or vertical_spacing == ""
                    or vertical_spacing < 0
                ):
                    self._errors["vertical_spacing"] = self.error_class(
                        ["Veuillez vérifier la valeur"]
                    )
                if (
                    horizontal_spacing is None
                    or horizontal_spacing == ""
                    or horizontal_spacing < 0
                ):
                    self._errors["horizontal_spacing"] = self.error_class(
                        ["Veuillez vérifier la valeur"]
                    )
            elif panel_implantation.id == 3:
                if (
                    vertical_overlapping is None
                    or vertical_overlapping == ""
                    or vertical_overlapping < 0
                ):
                    self._errors["vertical_overlapping"] = self.error_class(
                        ["Veuillez vérifier la valeur"]
                    )
                if (
                    horizontal_overlapping is None
                    or horizontal_overlapping == ""
                    or horizontal_overlapping < 0
                ):
                    self._errors["horizontal_overlapping"] = self.error_class(
                        ["Veuillez vérifier la valeur"]
                    )
        # return any errors if found
        return self.cleaned_data


class ConfigForm(ModelForm):
    class Meta:
        model = Config
        fields = (
            "inverter_id",
            "inverter_quantity",
        )

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        self.fields["inverter_quantity"].required = True
        self.fields["inverter_quantity"].widget.attrs.update(
            {"value": 0, "class": "cn config"}
        )
        self.fields["inverter_id"].widget.attrs.update(
            {"class": "container_100 round_input cn config"}
        )

    inverter_id = forms.ModelChoiceField(
        queryset=Inverter.objects.all(), label="Onduleur", required=True, initial=1,
    )

    def clean(self):
        # data from the form is fetched using super function
        super(ConfigForm, self).clean()

        # return any errors if found
        return self.cleaned_data


class MPPForm(ModelForm):
    class Meta:
        model = MPP
        fields = (
            "serial",
            "parallel",
        )

    def __init__(self, *args, **kwargs):
        super(MPPForm, self).__init__(*args, **kwargs)
        self.fields["serial"].required = True
        self.fields["serial"].widget.attrs.update({"value": 0, "class": "cn config"})
        self.fields["parallel"].required = True
        self.fields["parallel"].widget.attrs.update({"value": 0, "class": "cn config"})

    def clean(self):
        # data from the form is fetched using super function
        super(MPPForm, self).clean()

        # return any errors if found
        return self.cleaned_data
