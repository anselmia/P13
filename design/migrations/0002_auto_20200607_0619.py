# Generated by Django 3.0.4 on 2020-06-07 04:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("design", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="panel",
            name="manufacturer_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fabricant_panneau",
                to="design.Manufacturer",
            ),
        ),
        migrations.AddField(
            model_name="panel",
            name="technology_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="technologie_panneau",
                to="design.Technology",
            ),
        ),
        migrations.AddField(
            model_name="panel",
            name="temperature_factor_current_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="temp_coeff_current",
                to="design.Temperature_coefficient",
            ),
        ),
        migrations.AddField(
            model_name="panel",
            name="temperature_factor_power_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="temp_coeff_power",
                to="design.Temperature_coefficient",
            ),
        ),
        migrations.AddField(
            model_name="panel",
            name="temperature_factor_voltage_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="temp_coeff_voltage",
                to="design.Temperature_coefficient",
            ),
        ),
        migrations.AddField(
            model_name="mpp",
            name="config_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="config",
                to="design.Config",
            ),
        ),
        migrations.AddField(
            model_name="inverter",
            name="ac_cabling",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Raccordement",
                to="design.AC_connexion",
            ),
        ),
        migrations.AddField(
            model_name="inverter",
            name="manufacturer_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fabricant_onduleur",
                to="design.Manufacturer",
            ),
        ),
        migrations.AddField(
            model_name="implantation",
            name="panel_implantation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="panel_implantation",
                to="design.Pose",
            ),
        ),
        migrations.AddField(
            model_name="implantation",
            name="panel_orientation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="panel_orientation",
                to="design.Orientation",
            ),
        ),
        migrations.AddField(
            model_name="implantation",
            name="roof_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="roof_in_implantation",
                to="design.Roof",
            ),
        ),
        migrations.AddField(
            model_name="element",
            name="roof_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="roof",
                to="design.Roof",
            ),
        ),
        migrations.AddField(
            model_name="config",
            name="inverter_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="inverter",
                to="design.Inverter",
                verbose_name="Onduleur",
            ),
        ),
        migrations.AddField(
            model_name="config",
            name="project_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project_in_config",
                to="design.Project",
            ),
        ),
        migrations.AddConstraint(
            model_name="project",
            constraint=models.UniqueConstraint(
                fields=("name", "user_id"), name="unique_relation"
            ),
        ),
    ]
