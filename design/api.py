import requests
from django.conf import settings


class TemperatureData:
    """
        Class to communicate with google find place api
        Init with attribute search, place to find within the google aî
    """

    def __init__(self, city_name):
        """Init function of class Map"""

        self.name_tag_url = "https://api.meteostat.net/v1/stations/search?"
        self.temperature_url = "https://api.meteostat.net/v1/climate/normals?"
        self.city = city_name
        self.name_parameters = {
            "key": getattr(settings, "METEOSTAT_API_KEY", None),
            "q": city_name,
        }
        self.get_response()

    def get_response(self):
        """ request gmap api """

        request = requests.get(self.name_tag_url, params=self.name_parameters).json()
        if len(request) > 0:
            cities = request["data"]
            for city in cities:
                if city["country"] == "FR":
                    self.id_city = city["id"]
                    self.temperature_parameters = {
                        "key": getattr(settings, "METEOSTAT_API_KEY", None),
                        "station": self.id_city,
                    }
                    request = requests.get(
                        self.temperature_url, params=self.temperature_parameters
                    ).json()
                    if len(request) > 0:
                        temperatures = request["data"]["temperature"]
                        break
