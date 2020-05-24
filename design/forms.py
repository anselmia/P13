from django import forms
from project.models import City, Project
from .models import Panel
from user.models import User
from django.forms import ModelForm


class DesignForm_Step1(ModelForm):
    class Meta:
        model = Project
        fields = ("name", "building_type", "city_id", "panel_id", "user_id")

    def __init__(self, *args, **kwargs):
        super(DesignForm_Step1, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"class": "container_33"})
        self.fields["name"].required = True
        self.fields["building_type"].widget.attrs.update({"class": "container_33"})
        self.fields["building_type"].required = True

    city_id = forms.ModelChoiceField(
        queryset=City.objects.all(), label="Ville", required=True
    )
    city_id.widget.attrs["class"] = "round_select container_33"
    panel_id = forms.ModelChoiceField(
        queryset=Panel.objects.all(), label="Type de panneaux", required=True
    )
    panel_id.widget.attrs["class"] = "round_select container_33"
