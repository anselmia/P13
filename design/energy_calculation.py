import math
from .models import Panel, City
from calendar import monthrange
from datetime import date
from .api import EnergyData


class Production:
    def __init__(self, datas):
        self.monthly_prod = [0] * 12
        self.month = [
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "jun",
            "jul",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
        ]
        self.panel = Panel.objects.get(id=int(datas["panel_id"]))
        self.site = City.objects.get(id=int(datas["site_id"]))
        self.orientation = float(datas["orientation"])
        self.tilt = float(datas["tilt"])
        self.tot_panel = float(datas["tot_panel"])
        self.tot_power = self.tot_panel * self.panel.power / 1000
        self.lat = float(self.site.lat)
        self.lon = float(self.site.lon)
        self.get_production()

    def get_production(self):
        energy = EnergyData()
        self.datas = energy.get_ener(
            self.lat, self.lon, self.tot_power, self.tilt, self.orientation
        )
