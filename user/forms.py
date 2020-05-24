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
