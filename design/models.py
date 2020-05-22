from django.db import models

# Create your models here.


class Manufacturer(models.Model):
    """ Manufacturer """

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")

    class Meta:
        verbose_name = "Fabricant"
        verbose_name_plural = "Fabricants"

    def __str__(self):
        return self.name


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
    technology = models.IntegerField(blank=True, null=False)
    power = models.IntegerField(blank=True, null=False)
    tolerance = models.IntegerField(blank=True, null=False)
    radiation = models.IntegerField(blank=True, null=False)
    temperature = models.IntegerField(blank=True, null=False)
    short_circuit_current = models.DecimalField(
        max_digits=4, decimal_places=2, null=True
    )
    opent_circuit_voltage = models.DecimalField(
        max_digits=4, decimal_places=2, null=True
    )
    temperature_factor_current = models.DecimalField(
        max_digits=4, decimal_places=2, null=True
    )
    temperature_factor_voltage = models.DecimalField(
        max_digits=4, decimal_places=2, null=True
    )
    temperature_factor_power = models.DecimalField(
        max_digits=4, decimal_places=2, null=True
    )
    temperature_factor_current_type = models.IntegerField(blank=True, null=False)
    temperature_factor_voltage_type = models.IntegerField(blank=True, null=False)
    temperature_factor_power_type = models.IntegerField(blank=True, null=False)
    efficiency = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    mpp_current = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    mpp_voltage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    voltage_max = models.IntegerField(blank=True, null=False)
    length = models.IntegerField(blank=True, null=False)
    width = models.IntegerField(blank=True, null=False)
    surface = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    serial_cell_quantity = models.IntegerField(blank=True, null=False)
    parallel_cell_quantity = models.IntegerField(blank=True, null=False)
    cell_surface = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    total_cell_surface = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    cell_quantity = models.IntegerField(blank=True, null=False)
    comment = models.CharField(max_length=1000, unique=True, verbose_name="Commentaire")

    class Meta:
        verbose_name = "Panneau"
        verbose_name_plural = "Panneaux"

    def __str__(self):
        return self.model
