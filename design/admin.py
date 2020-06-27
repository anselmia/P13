from django.contrib import admin
from design.models import (
    City,
    MPP,
    Manufacturer,
    Technology,
    Roof,
    Roof_type,
    Orientation,
    Pose,
    Temperature_coefficient,
    AC_connexion,
    Inverter,
    Panel,
    Project,
    Implantation,
    Config,
)

admin.site.register(City)
admin.site.register(Manufacturer)
admin.site.register(Technology)
admin.site.register(Roof_type)
admin.site.register(Orientation)
admin.site.register(Pose)
admin.site.register(Temperature_coefficient)
admin.site.register(AC_connexion)
admin.site.register(Inverter)
admin.site.register(Panel)
admin.site.register(Project)
admin.site.register(Implantation)
admin.site.register(Roof)
admin.site.register(Config)
admin.site.register(MPP)
