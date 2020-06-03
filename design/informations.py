from .models import Panel, Inverter
from project.models import City


class Informations:
    def get_information(self, datas):
        panel = Panel.objects.get(id=int(datas["panel_id"]))
        pv_data = [
            panel.model,
            panel.power,
            round(panel.width * panel.length * int(datas["tot_pan"]) / 1000000, 1),
        ]
        site = City.objects.get(id=int(datas["site_id"]))
        site_data = [site.name, float(site.lat), float(site.lon)]
        inverter_ids = [0] * 3
        for config in datas["config"]:
            inverter_ids[int(config["index"]) - 1] = config["inverter_id"]
        inverters_datas = [
            [
                index,
                Inverter.objects.get(id=id).model,
                Inverter.objects.get(id=id).ac_power_nominal,
            ]
            for index, id in enumerate(inverter_ids)
            if id != 0
        ]

        return {
            "pv_data": pv_data,
            "site_data": site_data,
            "inverters_datas": inverters_datas,
        }
