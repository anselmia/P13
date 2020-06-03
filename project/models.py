from django.db import models
from user.models import User
from django.conf import settings


# Create your models here.


class City(models.Model):
    """ Projects """

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    lat = models.DecimalField(max_digits=9, decimal_places=7, verbose_name="Latitude")
    lon = models.DecimalField(max_digits=10, decimal_places=7, verbose_name="Longitude")

    class Meta:
        verbose_name = "Ville"
        verbose_name_plural = "Villes"

    def __str__(self):
        return self.name


class Project(models.Model):
    """ Projects """

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city_id = models.ForeignKey(
        City, related_name="ville", on_delete=models.CASCADE, verbose_name="Ville",
    )
    panel_id = models.ForeignKey(
        "design.Panel",
        related_name="panneau",
        on_delete=models.CASCADE,
        verbose_name=u"Type de panneau",
    )

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return self.name
