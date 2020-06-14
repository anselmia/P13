import requests
from django.conf import settings
import json


class Localisation:
    """
        API ressource to retrieve data from Opencagedata.
        Retrieve latitude and longitude from city name
    """

    def __init__(self, city_name):
        """Init function of class Localisation"""
        self.url = "https://api.opencagedata.com/geocode/v1/json?"
        self.city = city_name
        self.parameters = {
            "key": getattr(settings, "OPEN_CAGE_DATA_API_KEY", None),
            "q": city_name,
            "countrycode": "fr",
        }
        self.data = self.get_response()

    def get_response(self):
        """ request opencagedata api
            return city name, latitude and longitude if found,
            empty list if not
        """
        try:
            request = requests.get(self.url, params=self.parameters).json()
            cities = request["results"]
            if len(cities) > 0:
                for city in cities:
                    if city["components"]["country"] == "France":
                        datas = {
                            "name": city["components"]["city"],
                            "lat": city["geometry"]["lat"],
                            "lon": city["geometry"]["lng"],
                        }
                    return datas
        except:
            return []


class EnergyData:
    """
        API ressource to retrieve data from PVGis.
    """

    def get_ener(self, lat, lon, installation_power, tilt, orientation):
        """
            Given Latitude, Longitude, PV power, roof tilt and orientation,
            request PVGis Api to retrieve monthly average irradiation of the
            given site and monthly average photovoltaic production.

            When ok return list of monthly and yearly pv production and
            solar irradiation, ratio of system energy production by
            installed power (kWh/kWc).
            else empty list
        """
        self.parameters = {
            "lat": lat,
            "lon": lon,
            "peakpower": installation_power,
            "mountingplace": "building",
            "loss": 14,
            "angle": tilt,
            "aspect": orientation,
            "outputformat": "json",
        }
        self.pvgis = "https://re.jrc.ec.europa.eu/api/PVcalc?"

        try:
            request = requests.get(self.pvgis, params=self.parameters)
        except:
            return []

        text = json.loads(request.text)
        if len(text["outputs"]) > 0:
            try:

                datas = text["outputs"]["monthly"]["fixed"]
                monthly_irrad = [0] * 12
                monthly_prod = [0] * 12
                for month in range(12):
                    monthly_irrad[month] = datas[month]["H(i)_m"]
                    monthly_prod[month] = datas[month]["E_m"]

                yearly_prod = int(sum(monthly_prod))
                yearly_irrad = int(sum(monthly_irrad))
                ratio = round(yearly_prod / installation_power)

                return {
                    "monthly_irrad": monthly_irrad,
                    "monthly_prod": monthly_prod,
                    "yearly_prod": yearly_prod,
                    "yearly_irrad": yearly_irrad,
                    "ratio": ratio,
                }
            except:
                return []
