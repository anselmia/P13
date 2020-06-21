from .models import Panel, City
from .api import EnergyData


class Production:
    """ Class to process necessary datas to use with the PVGis api """

    def __init__(self, datas):
        """
        init expect : panel's id, site's id, roof orientation and tilt,
        total installed panel
        """
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
        """ Call PVGis Api and retrieve enrgy data related to the pv system """
        energy = EnergyData()
        self.datas = energy.get_ener(
            self.lat, self.lon, self.tot_power, self.tilt, self.orientation
        )
