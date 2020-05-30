from django.db import models
from project.models import Project

# Create your models here.


class Manufacturer(models.Model):
    """ Manufacturer """

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")

    class Meta:
        verbose_name = "Fabricant"
        verbose_name_plural = "Fabricants"

    def __str__(self):
        return self.name


class Technology(models.Model):
    """ Technology """

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")

    class Meta:
        verbose_name = "Technologie"
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name


class Roof_type(models.Model):
    """ Roof Type """

    value = models.CharField(max_length=30, unique=True, verbose_name="Type de toît")

    class Meta:
        verbose_name = "Type de Toît"

    def __str__(self):
        return self.value


class Roofing_type(models.Model):
    """ Roofing Type """

    value = models.CharField(max_length=30, unique=True, verbose_name="Type de Faîtage")

    class Meta:
        verbose_name = "Type de Faîtage"

    def __str__(self):
        return self.value


class Orientation(models.Model):
    """ Orientation Type """

    value = models.CharField(max_length=30, unique=True, verbose_name="Orientation")

    class Meta:
        verbose_name = "Orientation"

    def __str__(self):
        return self.value


class Pose(models.Model):
    """ Pose Type """

    value = models.CharField(max_length=30, unique=True, verbose_name="Pose")

    class Meta:
        verbose_name = " Pose"

    def __str__(self):
        return self.value


class Temperature_coefficient(models.Model):
    """ Technology """

    value = models.CharField(
        max_length=100, unique=True, verbose_name="Coeff. Temp. Type"
    )

    def __str__(self):
        return self.value


class Inverter(models.Model):
    """ Inverter """

    model = models.CharField(max_length=100, unique=True, verbose_name="Modèle")
    manufacturer_id = models.ForeignKey(
        Manufacturer, related_name="fabricant_onduleur", on_delete=models.CASCADE
    )
    mpp_voltage_min = models.IntegerField(blank=True, null=False)
    mpp_voltage_max = models.IntegerField(blank=True, null=False)
    dc_voltage_max = models.IntegerField(blank=True, null=False)
    dc_current_max = models.IntegerField(blank=True, null=False)
    dc_power_max = models.IntegerField(blank=True, null=False)
    ac_power_nominal = models.IntegerField(blank=True, null=False)
    ac_power_max = models.IntegerField(blank=True, null=False)
    ac_current_max = models.IntegerField(blank=True, null=False)
    efficiency = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    mpp_string_max = models.IntegerField(blank=True, null=False)
    mpp = models.IntegerField(blank=True, null=False)
    ac_cabling = models.IntegerField(blank=True, null=False)
    comment = models.CharField(max_length=1000, unique=True, verbose_name="Commentaire")

    class Meta:
        verbose_name = "Onduleur"
        verbose_name_plural = "Onduleurs"

    def __str__(self):
        return self.model


class Panel(models.Model):
    """ Panel """

    model = models.CharField(max_length=100, unique=True, verbose_name="Modèle")
    manufacturer_id = models.ForeignKey(
        Manufacturer, related_name="fabricant_panneau", on_delete=models.CASCADE
    )
    technology_id = models.ForeignKey(
        Technology, related_name="technologie_panneau", on_delete=models.CASCADE
    )
    power = models.IntegerField(blank=True, null=False, verbose_name="Puissance")
    tolerance = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, verbose_name="Tolérance"
    )
    radiation = models.IntegerField(
        blank=True, null=False, verbose_name="Rayonnement de référence"
    )
    temperature = models.IntegerField(
        blank=True, null=False, verbose_name="Température de référence"
    )
    short_circuit_current = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, verbose_name="Icc"
    )
    open_circuit_voltage = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, verbose_name="Vco"
    )
    temperature_factor_current = models.DecimalField(
        max_digits=6, decimal_places=3, null=True, verbose_name="Coeff. de Temp. I"
    )
    temperature_factor_current_type = models.ForeignKey(
        Temperature_coefficient,
        related_name="temp_coeff_current",
        on_delete=models.CASCADE,
    )
    temperature_factor_voltage = models.DecimalField(
        max_digits=6, decimal_places=3, null=True, verbose_name="Coeff. de Temp. V"
    )
    temperature_factor_voltage_type = models.ForeignKey(
        Temperature_coefficient,
        related_name="temp_coeff_voltage",
        on_delete=models.CASCADE,
    )
    temperature_factor_power = models.DecimalField(
        max_digits=6, decimal_places=3, null=True, verbose_name="Coeff. de Temp. P"
    )
    temperature_factor_power_type = models.ForeignKey(
        Temperature_coefficient,
        related_name="temp_coeff_power",
        on_delete=models.CASCADE,
    )
    mpp_current = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, verbose_name="Impp"
    )
    mpp_voltage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, verbose_name="Vmpp"
    )
    voltage_max = models.IntegerField(blank=True, null=False, verbose_name="Vmax")
    length = models.IntegerField(blank=True, null=False, verbose_name="Longueur")
    width = models.IntegerField(blank=True, null=False, verbose_name="Largeur")
    serial_cell_quantity = models.IntegerField(
        blank=True, null=False, verbose_name="Cell. en Série"
    )
    parallel_cell_quantity = models.IntegerField(
        blank=True, null=False, verbose_name="Cell. en Parallèle"
    )
    cell_surface = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, verbose_name="Surface d'une Cell."
    )
    comment = models.CharField(max_length=1000, verbose_name="Commentaire")

    class Meta:
        verbose_name = "Panneau"
        verbose_name_plural = "Panneaux"

    def __str__(self):
        return self.model


class Roof(models.Model):
    """ Projects """

    project_id = models.ForeignKey(
        Project, related_name="project", on_delete=models.CASCADE
    )

    roofing_type_id = models.ForeignKey(
        Roofing_type, related_name="roofing_type", on_delete=models.CASCADE
    )
    roof_type_id = models.ForeignKey(
        Roof_type, related_name="roof_type", on_delete=models.CASCADE
    )

    bottom_length = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, verbose_name="Longueur goutière (b)"
    )
    top_length = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Longueur faîtage (d)"
    )
    width = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, verbose_name="Rampant (a)"
    )
    height = models.DecimalField(
        max_digits=4, decimal_places=2, verbose_name="Hauteur (z)"
    )
    orientation = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Orientation"
    )
    tilt = models.DecimalField(
        max_digits=4, decimal_places=2, verbose_name="Inclinaison"
    )

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

    panel_orientation = models.ForeignKey(
        Orientation, related_name="panel_orientation", on_delete=models.CASCADE
    )
    panel_implantation = models.ForeignKey(
        Pose, related_name="panel_implantation", on_delete=models.CASCADE
    )

    vertical_overlapping = models.IntegerField(
        blank=True, null=False, verbose_name="Recouvrement vertical"
    )
    horizontal_overlapping = models.IntegerField(
        blank=True, null=False, verbose_name="Recouvrement horizontal"
    )
    vertical_spacing = models.IntegerField(
        blank=True, null=False, verbose_name="Espacement vertical"
    )
    horizontal_spacing = models.IntegerField(
        blank=True, null=False, verbose_name="Espacement horizontal"
    )
    distance_top = models.IntegerField(
        blank=True, null=False, verbose_name="Distance haut"
    )
    distance_bottom = models.IntegerField(
        blank=True, null=False, verbose_name="Distance bas"
    )
    distance_left = models.IntegerField(
        blank=True, null=False, verbose_name="Distance gauche"
    )
    distance_right = models.IntegerField(
        blank=True, null=False, verbose_name="Distance droite"
    )
    abergement_top = models.IntegerField(
        blank=True, null=False, verbose_name="Abergement Haut"
    )
    abergement_bottom = models.IntegerField(
        blank=True, null=False, verbose_name="Abergement bas"
    )
    abergement_left = models.IntegerField(
        blank=True, null=False, verbose_name="Abergement gauche"
    )
    abergement_right = models.IntegerField(
        blank=True, null=False, verbose_name="Abergement droit"
    )

    class Meta:
        verbose_name = "Implémentation"
        verbose_name_plural = "Implémentations"

    def __str__(self):
        return self.roof_id.project_id.name
