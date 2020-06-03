import requests
from django.conf import settings
from decimal import Decimal
import json


class Localisation:
    """
        Class to communicate with google find place api
        Init with attribute search, place to find within the google aî
    """

    def __init__(self, city_name):
        """Init function of class Map"""
        self.url = "https://api.opencagedata.com/geocode/v1/json?"
        self.city = city_name
        self.parameters = {
            "key": getattr(settings, "OPEN_CAGE_DATA_API_KEY", None),
            "q": city_name,
            "countrycode": "fr",
        }
        self.data = self.get_response()

    def get_response(self):
        """ request gmap api """
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
        except Exception as inst:
            return []


class EnergyData:
    """
        Class to communicate with google find place api
        Init with attribute search, place to find within the google aî
    """

    def __init__(self):
        """Init function of class Map"""

    def get_ener(self, lat, lon, installation_power, tilt, orientation):
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

                yearly_prod = sum(monthly_prod)
                yearly_irrad = sum(monthly_irrad)
                ratio = round(yearly_prod / installation_power, 1)

                return {
                    "monthly_irrad": monthly_irrad,
                    "monthly_prod": monthly_prod,
                    "yearly_prod": yearly_prod,
                    "yearly_irrad": yearly_irrad,
                    "ratio": ratio,
                }
            except Exception as e:
                return []
