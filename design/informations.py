from .models import (
    Panel,
    Inverter,
    City,
    Roof,
    Config,
    MPP,
)
from design.energy_calculation import Production


class Informations:
    """
        Class used to retrieved informations from models and make calculation
        to be used in design.js script to avoid client side calculation.
    """

    def get_production_information(self, datas):
        """ Data used in step 5 : Production """
        panel = Panel.objects.get(id=int(datas["panel_id"]))
        pv_data = [
            panel.model,
            panel.power,
            round(
                panel.width
                * panel.length
                * int(datas["tot_pan"])
                / 1000000,
                1,
            ),
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

    def get_projects_informations(self, projects):
        """ Data used in my projects  """
        datas = []

        for project in projects:
            try:
                site = City.objects.get(id=project.city_id.id)
                panel = Panel.objects.get(id=project.panel_id.id)
                roof = Roof.objects.get(project_id=project.id)
                configs = Config.objects.filter(project_id=project.id)
                tot_panel = 0

                for config in configs:
                    mpp_in_config = MPP.objects.filter(config_id=config.id)
                    for mpp in mpp_in_config:
                        tot_panel += (
                            config.inverter_quantity
                            * mpp.serial
                            * mpp.parallel
                        )

                data = {
                    "panel_id": panel.id,
                    "site_id": site.id,
                    "orientation": roof.orientation,
                    "tilt": roof.tilt,
                    "tot_panel": tot_panel,
                }
                project_prod = Production(data).datas

                datas.append(
                    {
                        "name": project.name,
                        "site": site.name,
                        "yearly_irrad": project_prod["yearly_irrad"],
                        "yearly_prod": project_prod["yearly_prod"],
                    }
                )
            except Exception:
                pass

        return datas
