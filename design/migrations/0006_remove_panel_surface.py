# Generated by Django 3.0.4 on 2020-05-26 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0005_remove_panel_efficiency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='panel',
            name='surface',
        ),
    ]
