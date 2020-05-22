# Generated by Django 3.0.4 on 2020-05-22 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nom')),
            ],
            options={
                'verbose_name': 'Fabricant',
                'verbose_name_plural': 'Fabricants',
            },
        ),
        migrations.CreateModel(
            name='Panel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, unique=True, verbose_name='Modèle')),
                ('technology', models.IntegerField(blank=True)),
                ('power', models.IntegerField(blank=True)),
                ('tolerance', models.IntegerField(blank=True)),
                ('radiation', models.IntegerField(blank=True)),
                ('temperature', models.IntegerField(blank=True)),
                ('short_circuit_current', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('opent_circuit_voltage', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('temperature_factor_current', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('temperature_factor_voltage', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('temperature_factor_power', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('temperature_factor_current_type', models.IntegerField(blank=True)),
                ('temperature_factor_voltage_type', models.IntegerField(blank=True)),
                ('temperature_factor_power_type', models.IntegerField(blank=True)),
                ('efficiency', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('mpp_current', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('mpp_voltage', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('voltage_max', models.IntegerField(blank=True)),
                ('length', models.IntegerField(blank=True)),
                ('width', models.IntegerField(blank=True)),
                ('surface', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('serial_cell_quantity', models.IntegerField(blank=True)),
                ('parallel_cell_quantity', models.IntegerField(blank=True)),
                ('cell_surface', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('total_cell_surface', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('cell_quantity', models.IntegerField(blank=True)),
                ('comment', models.CharField(max_length=1000, unique=True, verbose_name='Commentaire')),
                ('manufacturer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fabricant_panneau', to='design.Manufacturer')),
            ],
            options={
                'verbose_name': 'Panneau',
                'verbose_name_plural': 'Panneaux',
            },
        ),
        migrations.CreateModel(
            name='Inverter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, unique=True, verbose_name='Modèle')),
                ('mpp_voltage_min', models.IntegerField(blank=True)),
                ('mpp_voltage_max', models.IntegerField(blank=True)),
                ('dc_voltage_max', models.IntegerField(blank=True)),
                ('dc_current_max', models.IntegerField(blank=True)),
                ('dc_power_max', models.IntegerField(blank=True)),
                ('ac_power_nominal', models.IntegerField(blank=True)),
                ('ac_power_max', models.IntegerField(blank=True)),
                ('ac_current_max', models.IntegerField(blank=True)),
                ('efficiency', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('mpp_string_max', models.IntegerField(blank=True)),
                ('mpp', models.IntegerField(blank=True)),
                ('ac_cabling', models.IntegerField(blank=True)),
                ('comment', models.CharField(max_length=1000, unique=True, verbose_name='Commentaire')),
                ('manufacturer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fabricant_onduleur', to='design.Manufacturer')),
            ],
            options={
                'verbose_name': 'Onduleur',
                'verbose_name_plural': 'Onduleurs',
            },
        ),
    ]
