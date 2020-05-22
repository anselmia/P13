from django.db import models
from user.models import User
from design.models import Panel
from django.conf import settings

# Create your models here.


class City(models.Model):
    """ Projects """

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    average_temp_january = models.DecimalField(
        max_digits=3, decimal_places=1, null=False
    )
    average_temp_february = models.DecimalField(
        max_digits=3, decimal_places=1, null=False
    )
    average_temp_march = models.DecimalField(max_digits=3, decimal_places=1, null=False)
    average_temp_april = models.DecimalField(max_digits=3, decimal_places=1, null=False)
    average_temp_may = models.DecimalField(max_digits=3, decimal_places=1, null=False)
    average_temp_june = models.DecimalField(max_digits=3, decimal_places=1, null=False)
    average_temp_july = models.DecimalField(max_digits=3, decimal_places=1, null=False)
    average_temp_august = models.DecimalField(
        max_digits=3, decimal_places=1, null=False
    )
    average_temp_september = models.DecimalField(
        max_digits=3, decimal_places=1, null=False
    )
    average_temp_october = models.DecimalField(
        max_digits=3, decimal_places=1, null=False
    )
    average_temp_november = models.DecimalField(
        max_digits=3, decimal_places=1, null=False
    )
    average_temp_december = models.DecimalField(
        max_digits=3, decimal_places=1, null=False
    )

    class Meta:
        verbose_name = "Ville"
        verbose_name_plural = "Villes"

    def __str__(self):
        return self.name


class Project(models.Model):
    """ Projects """

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    building_type = models.IntegerField(blank=True, null=False)
    city_id = models.ForeignKey(City, related_name="project", on_delete=models.CASCADE)
    panel_id = models.ForeignKey(
        Panel, related_name="panneau", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return self.name


class Roof(models.Model):
    """ Projects """

    project_id = models.ForeignKey(
        Project, related_name="project", on_delete=models.CASCADE
    )

    roofing_type = models.IntegerField(blank=True, null=False)
    roof_type = models.IntegerField(blank=True, null=False)

    length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    surface = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    orientation = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    tilt = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    class Meta:
        verbose_name = "Toît"
        verbose_name_plural = "Toîts"

    def __str__(self):
        return self.project_id.name


class Element(models.Model):
    """ Element """

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    roof_id = models.ForeignKey(Roof, related_name="roof", on_delete=models.CASCADE)

    left_distance = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    bottom_distance = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        verbose_name = "Element"
        verbose_name_plural = "Elements"

    def __str__(self):
        return self.project_id.name


class Implantation(models.Model):
    """ Implementation """

    roof_id = models.ForeignKey(Roof, related_name="project", on_delete=models.CASCADE)

    panel_orientation = models.IntegerField(blank=True, null=False)
    panel_implantation = models.IntegerField(blank=True, null=False)

    vertical_overlapping = models.IntegerField(blank=True, null=False)
    horizontal_overlapping = models.IntegerField(blank=True, null=False)
    vertical_spacing = models.IntegerField(blank=True, null=False)
    horizontal_spacing = models.IntegerField(blank=True, null=False)
    distance_top = models.IntegerField(blank=True, null=False)
    distance_bottom = models.IntegerField(blank=True, null=False)
    distance_left = models.IntegerField(blank=True, null=False)
    distance_right = models.IntegerField(blank=True, null=False)
    abergement_top = models.IntegerField(blank=True, null=False)
    abergement_bottom = models.IntegerField(blank=True, null=False)
    abergement_left = models.IntegerField(blank=True, null=False)
    abergement_right = models.IntegerField(blank=True, null=False)

    class Meta:
        verbose_name = "Implémentation"
        verbose_name_plural = "Implémentations"

    def __str__(self):
        return self.roof_id.project_id.name
