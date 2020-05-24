from django.shortcuts import render
from .forms import DesignForm_Step1
from django.contrib.auth.decorators import login_required
from design.api import TemperatureData

# Create your views here.


@login_required
def index(request):
    """
    Views for home
    :param request:
    :return render home.html:
    """
    if request.method == "POST":
        project = DesignForm_Step1(data=request.POST)
        try:
            if project.is_valid():
                project.save(commit=False)
                project.user_id = request.user
                project.save()
        except:
            pass
    else:
        project = DesignForm_Step1()

    return render(request, "index.html", {"form_project": project,})


# def get_city_data(request):
