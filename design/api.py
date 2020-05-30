import requests
from django.conf import settings
from decimal import Decimal


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
                    if city["components"]["city"].lower() == self.city.lower():
                        datas = {
                            "city": city["components"]["city"],
                            "lat": city["geometry"]["lat"],
                            "lon": city["geometry"]["lng"],
                        }
                    return datas
        except Exception as inst:
            return []


class TemperatureData:
    """
        Class to communicate with google find place api
        Init with attribute search, place to find within the google aî
    """

    def __init__(self, city_name):
        """Init function of class Map"""
        self.name_tag_url = "https://api.meteostat.net/v1/stations/search?"
        self.temperature_url = "https://api.meteostat.net/v1/climate/normals?"
        self.test_url = "https://api.meteostat.net/v1/stations/meta?"
        self.city = city_name
        self.name_parameters = {
            "key": getattr(settings, "METEOSTAT_API_KEY", None),
            "q": city_name,
        }
        self.data = self.get_response()

    def get_response(self):
        """ request gmap api """

        request = requests.get(self.name_tag_url, params=self.name_parameters).json()
        if len(request) > 0:
            cities = request["data"]
            for city in cities:
                if city["country"] == "FR":
                    self.id_city = city["id"]
                    self.test_parameters = {
                        "key": getattr(settings, "METEOSTAT_API_KEY", None),
                        "station": self.id_city,
                        "inventory": 1,
                    }
                    request = requests.get(
                        self.test_url, params=self.test_parameters
                    ).json()
                    Lat = request["data"]["latitude"]
                    Longitude = request["data"]["longitude"]
                    self.temperature_parameters = {
                        "key": getattr(settings, "METEOSTAT_API_KEY", None),
                        "station": self.id_city,
                    }
                    request = requests.get(
                        self.temperature_url, params=self.temperature_parameters
                    ).json()
                    if len(request) > 0:
                        datas = {
                            "temperatures": request["data"]["temperature"],
                            "lat": Lat,
                            "lon": Longitude,
                        }
                        return datas

        return []


class IrradianceData:
    """
        Class to communicate with google find place api
        Init with attribute search, place to find within the google aî
    """

    def __init__(self, Lat, Lon):
        """Init function of class Map"""
        lat = float(Lat)
        lon = float(Lon)

        self.irradiance_url = "https://developer.nrel.gov/api/pvwatts/v6.json?"
        self.irradiance_url = "https://developer.nrel.gov/api/solar/data_query/v1.json?"
        self.parameters = {
            "api_key": getattr(settings, "NREL_API_KEY", None),
            "lat": lat,
            "lon": lon,
            "radius": 0,
        }
        request = requests.get(self.irradiance_url, params=self.parameters).json()
        outputs = request["outputs"]
        intl_station = outputs["intl"]
        station_id = intl_station["id"]
        self.irradiance_url = "https://developer.nrel.gov/api/pvwatts/v6.json?"
        self.parameters = {
            "api_key": getattr(settings, "NREL_API_KEY", None),
            "file_id": station_id,
            "radius": 300,
            "system_capacity": 3,
            "module_type": 0,
            "losses": 0,
            "array_type": 0,
            "tilt": 30,
            "azimuth": 0,
        }
        self.data = self.get_response()

    def get_response(self):
        """ request gmap api """
        try:
            request = requests.get(self.irradiance_url, params=self.parameters).json()
            request.raise_for_status()

        except requests.exceptions.HTTPError as err:
            pass
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.TooManyRedirects:
            pass
        except requests.exceptions.RequestException as e:
            pass

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
                        return temperatures

        return []
