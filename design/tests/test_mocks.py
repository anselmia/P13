from design import api
import requests
from django.test import TestCase
from unittest import mock


class test(TestCase):
    def test_request_opencagedata(monkeypatch):
        """ Mock request gmap """
        result = [
            {
                "annotations": {
                    "DMS": {
                        "lat": "47° 13' 7.09356'' N",
                        "lng": "1° 33' 14.89032'' W",
                    },
                    "MGRS": "30TXT0947230474",
                    "Maidenhead": "IN97ff32ml",
                    "Mercator": {"x": -173005.65, "y": 5946458.772},
                    "OSM": {
                        "edit_url": "https://www.openstre...4/-1.55414",
                        "note_url": "https://www.openstre...4&layers=N",
                        "url": "https://www.openstre...4/-1.55414",
                    },
                    "UN_M49": {"regions": {}, "statistical_groupings": []},
                    "callingcode": 33,
                    "currency": {
                        "alternate_symbols": [],
                        "decimal_mark": ",",
                        "html_entity": "&#x20AC;",
                        "iso_code": "EUR",
                        "iso_numeric": "978",
                        "name": "Euro",
                        "smallest_denomination": 1,
                        "subunit": "Cent",
                        "subunit_to_unit": 100,
                    },
                    "flag": "🇫🇷",
                    "geohash": "gbquseuk6pbjcf41wyq0",
                    "qibla": 113.27,
                    "roadinfo": {"drive_on": "right", "speed_in": "km/h"},
                    "sun": {"rise": {}, "set": {}},
                    "timezone": {
                        "name": "Europe/Paris",
                        "now_in_dst": 1,
                        "offset_sec": 7200,
                        "offset_string": "+0200",
                        "short_name": "CEST",
                    },
                    "bounds": {
                        "northeast": {
                            "lat": 47.2958583,
                            "lng": -1.4788443,
                        },
                        "southwest": {
                            "lat": 47.1805856,
                            "lng": -1.6418115,
                        },
                    },
                    "components": {
                        "ISO_3166-1_alpha-2": "FR",
                        "ISO_3166-1_alpha-3": "FRA",
                        "_category": "place",
                        "_type": "city",
                        "city": "Nantes",
                        "continent": "Europe",
                        "country": "France",
                        "country_code": "fr",
                        "county": "Nantes",
                        "political_union": "European Union",
                        "state": "Pays de la Loire",
                        "state_code": "PDL",
                        "state_district": "Loire-Atlantique",
                    },
                    "confidence": 6,
                    "formatted": "Nantes, France",
                    "geometry": {"lat": 47.2186371, "lng": -1.5541362},
                },
            }
        ]

        def mock_return(url, params):
            """ gmap Mock response """
            return MockResponse(
                {
                    "annotations": {
                        "DMS": {
                            "lat": "47° 13' 7.09356'' N",
                            "lng": "1° 33' 14.89032'' W",
                        },
                        "MGRS": "30TXT0947230474",
                        "Maidenhead": "IN97ff32ml",
                        "Mercator": {"x": -173005.65, "y": 5946458.772},
                        "OSM": {
                            "edit_url": "https://www.openstre...4/-1.55414",
                            "note_url": "https://www.openstre...4&layers=N",
                            "url": "https://www.openstre...4/-1.55414",
                        },
                        "UN_M49": {
                            "regions": {},
                            "statistical_groupings": [],
                        },
                        "callingcode": 33,
                        "currency": {
                            "alternate_symbols": [],
                            "decimal_mark": ",",
                            "html_entity": "&#x20AC;",
                            "iso_code": "EUR",
                            "iso_numeric": "978",
                            "name": "Euro",
                            "smallest_denomination": 1,
                            "subunit": "Cent",
                            "subunit_to_unit": 100,
                        },
                        "flag": "🇫🇷",
                        "geohash": "gbquseuk6pbjcf41wyq0",
                        "qibla": 113.27,
                        "roadinfo": {
                            "drive_on": "right",
                            "speed_in": "km/h",
                        },
                        "sun": {"rise": {}, "set": {}},
                        "timezone": {
                            "name": "Europe/Paris",
                            "now_in_dst": 1,
                            "offset_sec": 7200,
                            "offset_string": "+0200",
                            "short_name": "CEST",
                        },
                        "bounds": {
                            "northeast": {
                                "lat": 47.2958583,
                                "lng": -1.4788443,
                            },
                            "southwest": {
                                "lat": 47.1805856,
                                "lng": -1.6418115,
                            },
                        },
                        "components": {
                            "ISO_3166-1_alpha-2": "FR",
                            "ISO_3166-1_alpha-3": "FRA",
                            "_category": "place",
                            "_type": "city",
                            "city": "Nantes",
                            "continent": "Europe",
                            "country": "France",
                            "country_code": "fr",
                            "county": "Nantes",
                            "political_union": "European Union",
                            "state": "Pays de la Loire",
                            "state_code": "PDL",
                            "state_district": "Loire-Atlantique",
                        },
                        "confidence": 6,
                        "formatted": "Nantes, France",
                        "geometry": {"lat": 47.2186371, "lng": -1.5541362},
                    },
                }
            )

        monkeypatch.setattr(requests, "get", mock_return)
        loc = api.Localisation("Nantes")
        datas = loc.get_response()

        assert datas["lat"] == result[0]["components"]["geometry"][lat]


class MockResponse:
    """Mock for requests.get response call"""

    def __init__(self, result, ok=True):
        self.ok = ok
        self.result = result

    def json(self):
        """ Json function for mock class """
        return self.result
