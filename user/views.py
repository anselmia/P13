""" Imports """

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import ConnexionForm, UserUpdateForm, SignUpForm
from design.models import Project
from design.informations import Informations
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .forms import Project_information


@login_required
def profile(request):
    """
    @require login
    Views for profile
    :param request:
    :return render profile.html:
    """

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        try:
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Les modifications de votre profil ont bien été enregistrées",
                )
        except:  # pragma: no cover
            messages.error(
                request,
                "Erreurs durant l'enregistrement des informations de votre profil",
            )
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "profile.html", {"form": form,})


def login(request):
    """
    Views for login
    :param request:
    :return
    if method post and login ok
        if previous page exist : render last visited page
        else: render home.html
    else
        render login.html
    :
    """
    if request.user.is_authenticated:
        return redirect(reverse("home:index"))
    else:
        if request.method == "POST":
            form = ConnexionForm(data=request.POST)
            try:
                if form.is_valid():
                    user = authenticate(
                        username=form.cleaned_data["username"],
                        password=form.cleaned_data["password"],
                    )
                    try:
                        if user:
                            auth_login(request, user)
                            request.session.set_expiry(900)
                            return HttpResponseRedirect(request.session["previous"])
                        else:
                            messages.error(request, "Mauvais login/mot de passe.")
                            return render(request, "login.html", {"form": form})
                    except:  # pragma: no cover
                        redirect(reverse("home:index"))
            except Exception as e:  # pragma: no cover
                messages.error(request, "Erreur de login.")
                return render(request, "login.html", {"form": form})
        else:
            form = ConnexionForm(None)
            request.session["previous"] = request.META.get("HTTP_REFERER")

        return render(request, "login.html", {"form": form,})


def register(request):
    """
    Views for register
    :param request:
    :return
    if method post and form valid
        create user, login and redirect to home.html
    else
        render register.html
    :
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)
                auth_login(request, user)
                return redirect(reverse("home:index"))

        except Exception as e:
            messages.error(request, "Votre compte n'a pas été crée.")
    else:
        form = SignUpForm(None)

    return render(request, "register.html", {"form": form,})


@login_required
def project(request):
    """
    @require login
    Views for projects
    :param request:
    :return render projects.html:
    """
    projects = Project.objects.filter(user_id=request.user)
    projects = list(projects)
    info = Informations()
    projects_informations = info.get_projects_informations(projects)

    projectsFormSet = formset_factory(Project_information, extra=len(projects) - 1)
    formset = projectsFormSet(
        initial=[
            {
                "name": project_informations["name"],
                "site": project_informations["site"],
                "yearly_irrad": project_informations["yearly_irrad"],
                "yearly_prod": project_informations["yearly_prod"],
            }
            for project_informations in projects_informations
        ]
    )

    return render(
        request, "projects.html", {"title": "Mes Projets", "projects": formset,},
    )


@login_required
def logout(request):
    """
    @require login
    Views for logout
    :param request:
    :return reditrect to home.html:
    """
    auth_logout(request)
    return redirect(reverse("home:index"))
