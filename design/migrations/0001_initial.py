# Generated by Django 3.0.4 on 2020-06-07 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AC_connexion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ac_type', models.CharField(max_length=100, unique=True, verbose_name='Raccordement')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nom')),
                ('lat', models.DecimalField(decimal_places=7, max_digits=9, verbose_name='Latitude')),
                ('lon', models.DecimalField(decimal_places=7, max_digits=10, verbose_name='Longitude')),
            ],
            options={
                'verbose_name': 'Ville',
                'verbose_name_plural': 'Villes',
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inverter_quantity', models.IntegerField(blank=True, verbose_name="Nombre d'onduleurs")),
                ('index', models.IntegerField(blank=True, verbose_name='Index configuration')),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configurations',
            },
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nom')),
                ('left_distance', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('bottom_distance', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('length', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('width', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'verbose_name': 'Element',
                'verbose_name_plural': 'Elements',
            },
        ),
        migrations.CreateModel(
            name='Implantation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vertical_overlapping', models.IntegerField(blank=True, verbose_name='Recouvrement vertical')),
                ('horizontal_overlapping', models.IntegerField(blank=True, verbose_name='Recouvrement horizontal')),
                ('vertical_spacing', models.IntegerField(blank=True, verbose_name='Espacement vertical')),
                ('horizontal_spacing', models.IntegerField(blank=True, verbose_name='Espacement horizontal')),
                ('distance_top', models.IntegerField(blank=True, verbose_name='Distance haut')),
                ('distance_bottom', models.IntegerField(blank=True, verbose_name='Distance bas')),
                ('distance_left', models.IntegerField(blank=True, verbose_name='Distance gauche')),
                ('distance_right', models.IntegerField(blank=True, verbose_name='Distance droite')),
                ('abergement_top', models.IntegerField(blank=True, verbose_name='Abergement Haut')),
                ('abergement_bottom', models.IntegerField(blank=True, verbose_name='Abergement bas')),
                ('abergement_left', models.IntegerField(blank=True, verbose_name='Abergement gauche')),
                ('abergement_right', models.IntegerField(blank=True, verbose_name='Abergement droit')),
            ],
            options={
                'verbose_name': 'Implémentation',
                'verbose_name_plural': 'Implémentations',
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
                ('dc_current_max', models.DecimalField(decimal_places=2, max_digits=5)),
                ('dc_power_max', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ac_power_nominal', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ac_power_max', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('ac_current_max', models.DecimalField(decimal_places=2, max_digits=5)),
                ('efficiency', models.DecimalField(decimal_places=2, max_digits=4)),
                ('mpp_string_max', models.IntegerField(blank=True, null=True)),
                ('mpp', models.IntegerField(blank=True)),
                ('comment', models.CharField(blank=True, max_length=1000, null=True, unique=True, verbose_name='Commentaire')),
            ],
            options={
                'verbose_name': 'Onduleur',
                'verbose_name_plural': 'Onduleurs',
            },
        ),
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
            name='MPP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.IntegerField(blank=True, verbose_name='En série')),
                ('parallel', models.IntegerField(blank=True, verbose_name='En parallèle')),
            ],
            options={
                'verbose_name': 'MPP',
                'verbose_name_plural': 'MPPs',
            },
        ),
        migrations.CreateModel(
            name='Orientation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=30, unique=True, verbose_name='Orientation')),
            ],
            options={
                'verbose_name': 'Orientation',
            },
        ),
        migrations.CreateModel(
            name='Panel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, unique=True, verbose_name='Modèle')),
                ('power', models.IntegerField(blank=True, verbose_name='Puissance')),
                ('tolerance', models.DecimalField(decimal_places=2, max_digits=3, null=True, verbose_name='Tolérance')),
                ('radiation', models.IntegerField(blank=True, verbose_name='Rayonnement de référence')),
                ('temperature', models.IntegerField(blank=True, verbose_name='Température de référence')),
                ('short_circuit_current', models.DecimalField(decimal_places=2, max_digits=4, null=True, verbose_name='Icc')),
                ('open_circuit_voltage', models.DecimalField(decimal_places=2, max_digits=4, null=True, verbose_name='Vco')),
                ('temperature_factor_current', models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='Coeff. de Temp. I')),
                ('temperature_factor_voltage', models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='Coeff. de Temp. V')),
                ('temperature_factor_power', models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='Coeff. de Temp. P')),
                ('mpp_current', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Impp')),
                ('mpp_voltage', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Vmpp')),
                ('voltage_max', models.IntegerField(blank=True, verbose_name='Vmax')),
                ('length', models.IntegerField(blank=True, verbose_name='Longueur')),
                ('width', models.IntegerField(blank=True, verbose_name='Largeur')),
                ('serial_cell_quantity', models.IntegerField(blank=True, verbose_name='Cell. en Série')),
                ('parallel_cell_quantity', models.IntegerField(blank=True, verbose_name='Cell. en Parallèle')),
                ('cell_surface', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name="Surface d'une Cell.")),
                ('comment', models.CharField(max_length=1000, verbose_name='Commentaire')),
            ],
            options={
                'verbose_name': 'Panneau',
                'verbose_name_plural': 'Panneaux',
            },
        ),
        migrations.CreateModel(
            name='Pose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=30, unique=True, verbose_name='Pose')),
            ],
            options={
                'verbose_name': ' Pose',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ville', to='design.City', verbose_name='Ville')),
                ('panel_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='panneau_project', to='design.Panel', verbose_name='Type de panneau')),
            ],
            options={
                'verbose_name': 'Projet',
                'verbose_name_plural': 'Projets',
            },
        ),
        migrations.CreateModel(
            name='Roof_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=30, unique=True, verbose_name='Type de toît')),
            ],
            options={
                'verbose_name': 'Type de Toît',
            },
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nom')),
            ],
            options={
                'verbose_name': 'Technologie',
                'verbose_name_plural': 'Technologies',
            },
        ),
        migrations.CreateModel(
            name='Temperature_coefficient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100, unique=True, verbose_name='Coeff. Temp. Type')),
            ],
        ),
        migrations.CreateModel(
            name='Roof',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bottom_length', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Longueur goutière (b)')),
                ('top_length', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Longueur faîtage (d)')),
                ('width', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Rampant (a)')),
                ('height', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Hauteur (z)')),
                ('orientation', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Orientation')),
                ('tilt', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Inclinaison')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project', to='design.Project')),
                ('roof_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roof_type', to='design.Roof_type')),
            ],
            options={
                'verbose_name': 'Toît',
                'verbose_name_plural': 'Toîts',
            },
        ),
    ]
