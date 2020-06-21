""" Home Views """

from django.shortcuts import render

# Create your views here.


def home(request):
    """
    Views for home
    :param request:
    :return render home.html:
    """
    return render(request, "home.html")


def mentions(request):
    """
    Views for mentions
    :param request:
    :return render mentions.html:
    """
    return render(request, "mentions.html")
