from django import forms
from user.models import User
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
    AuthenticationForm,
)


class ConnexionForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text="Rentrer une adresse email valide"
    )
    robot = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email")


class Project_information(forms.Form):
    """ Form to retrieve project informations """

    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "name": "name",
                "readonly": True,
                "label": "Nom du projet",
            }
        ),
    )

    site = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"name": "city", "readonly": True, "label": "Ville"}
        ),
    )

    yearly_irrad = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "name": "yearly_irrad",
                "readonly": True,
                "label": "Irradiation annuelle",
            }
        ),
    )

    yearly_prod = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "name": "yearly_prod",
                "readonly": True,
                "label": "Production annuelle",
            }
        ),
    )
