from .models import Inverter, Panel
import json


class Calculation:
    def __init__(self, datas):
        self.tot_installed_panel = int(datas["tot_panel"])
        self.panel = Panel.objects.get(id=int(datas["panel_id"]))
        self.tot_configured_panel = 0
        self.tot_ac_nom_power = 0
        self.configs = []

        for config in datas["configs"]:
            configuration = Configuration(config, self.panel)
            self.configs.append(configuration)

        self.calculate_tot_panel()
        self.calculate_tot_ac_nom_power()
        self.rest_panel = self.tot_installed_panel - self.tot_configured_panel
        self.tot_power = (self.tot_installed_panel * self.panel.power) / 1000

        self.panel = None
        for config in self.configs:
            config.panel = None
            config.inverter = None

        self.data = self.toJSON()

    def calculate_tot_panel(self):
        self.tot_configured_panel = 0
        for config in self.configs:
            self.tot_configured_panel += config.tot_panel * config.inverter_quantity

    def calculate_tot_ac_nom_power(self):
        self.tot_ac_nom_power = 0
        for config in self.configs:
            self.tot_ac_nom_power += config.tot_nom_ac_power

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Configuration:
    def __init__(self, config, panel):
        self.index = int(config["index"])
        self.panel = panel
        self.inverter = Inverter.objects.get(id=int(config["inverter_id"]))
        self.inverter_quantity = int(config["inverter_quantity"])
        self.mpps = []
        self.icc_tot_at__10 = 0
        self.icc_tot_at_70 = 0

        for mpp in config["mpps"]:
            Mpp = MPP(mpp, self.panel)
            self.mpps.append(Mpp)

        self.Calculate_Config()

    def Calculate_Config(self):
        self.tot_panel = 0
        for mpp in self.mpps:
            self.tot_panel += mpp.serial * mpp.parallel
            self.icc_tot_at__10 += mpp.icc_at__10
            self.icc_tot_at_70 += mpp.icc_at_70

        self.tot_nom_ac_power = self.inverter_quantity * float(
            self.inverter.ac_power_nominal
        )
        self.tot_nom_dc_power = self.inverter_quantity * float(
            self.inverter.dc_power_max
        )
        self.tot_dc_power = (
            self.inverter_quantity * self.tot_panel * self.panel.power / 1000
        )
        self.power_ratio = (self.tot_dc_power / self.tot_nom_ac_power) * 100

        self.errors = []
        for mpp in self.mpps:
            if not (
                mpp.mpp_string_voltage_at_70 > self.inverter.mpp_voltage_min
                and mpp.mpp_string_voltage_at_70 < self.inverter.mpp_voltage_max
            ):
                self.errors.append(
                    [
                        ".inverter" + str(self.index) + "_mpp" + str(mpp.index),
                        ".mpp_voltage_min_value",
                    ]
                )
            if not (
                mpp.mpp_string_voltage_at__10 > self.inverter.mpp_voltage_min
                and mpp.mpp_string_voltage_at__10 < self.inverter.mpp_voltage_max
            ):
                self.errors.append(
                    [
                        ".inverter" + str(self.index) + "_mpp" + str(mpp.index),
                        ".mpp_voltage_max_value",
                    ]
                )
            if not (
                mpp.vco_string_voltage_at_70 < self.inverter.dc_voltage_max
                and mpp.vco_string_voltage_at_70 < self.panel.voltage_max
            ):
                self.errors.append(
                    [
                        ".inverter" + str(self.index) + "_mpp" + str(mpp.index),
                        ".vco_voltage_min_value",
                    ]
                )
            if not (
                mpp.vco_string_voltage_at__10 < self.inverter.dc_voltage_max
                and mpp.vco_string_voltage_at__10 < self.panel.voltage_max
            ):
                self.errors.append(
                    [
                        ".inverter" + str(self.index) + "_mpp" + str(mpp.index),
                        ".vco_voltage_max_value",
                    ]
                )
            if not (mpp.icc_at__10 < self.inverter.dc_current_max):
                self.errors.append(
                    [
                        ".inverter" + str(self.index) + "_mpp" + str(mpp.index),
                        ".i_min_value",
                    ]
                )
            if not (mpp.icc_at_70 < self.inverter.dc_current_max):
                self.errors.append(
                    [
                        ".inverter" + str(self.index) + "_mpp" + str(mpp.index),
                        ".i_max_value",
                    ]
                )

        if not (self.icc_tot_at_70 < self.inverter.dc_current_max):
            self.errors.append(".i_tot_max_value")
        if not (self.icc_tot_at__10 < self.inverter.dc_current_max):
            self.errors.append(".i_tot_min_value")
        if not (self.power_ratio >= 70 and self.power_ratio <= 130):
            self.errors.append(".ratio_pn_value")


class MPP:
    def __init__(self, mpp, panel):
        self.index = int(mpp["index"])
        self.serial = int(mpp["serial"])
        self.parallel = int(mpp["parallel"])
        self.power = self.string_power(panel)

        self.mpp_string_voltage_at_70 = self.string_mpp_voltage_at_temp(70, panel)
        self.mpp_string_voltage_at__10 = self.string_mpp_voltage_at_temp(-10, panel)

        self.vco_string_voltage_at_70 = self.string_vco_voltage_at_temp(70, panel)
        self.vco_string_voltage_at__10 = self.string_vco_voltage_at_temp(-10, panel)

        self.icc_at__10 = self.icc_at_temp(-10, panel)
        self.icc_at_70 = self.icc_at_temp(70, panel)

    def string_power(self, panel):
        return self.serial * panel.power

    def string_mpp_voltage_at_temp(self, temp, panel):
        if panel.temperature_factor_voltage_type_id == 1:
            return (
                float(panel.mpp_voltage)
                + (
                    (float(panel.mpp_voltage) / 100)
                    * float(panel.temperature_factor_voltage)
                    * (temp - panel.temperature)
                )
            ) * self.serial
        else:
            return (
                float(panel.mpp_voltage)
                + (
                    (float(panel.temperature_factor_voltage) / 1000)
                    * (temp - panel.temperature)
                )
            ) * self.serial

    def string_vco_voltage_at_temp(self, temp, panel):
        if panel.temperature_factor_voltage_type_id == 1:
            return (
                float(panel.open_circuit_voltage)
                + (
                    (float(panel.open_circuit_voltage) / 100)
                    * float(panel.temperature_factor_voltage)
                    * (temp - panel.temperature)
                )
            ) * self.serial
        else:
            return (
                float(panel.open_circuit_voltage)
                + (
                    (float(panel.temperature_factor_voltage) / 1000)
                    * (temp - panel.temperature)
                )
            ) * self.serial

    def icc_at_temp(self, temp, panel):
        if panel.temperature_factor_current_type_id == 1:
            return (
                float(panel.short_circuit_current)
                + (
                    (float(panel.short_circuit_current) / 100)
                    * float(panel.temperature_factor_current)
                    * (temp - panel.temperature)
                )
            ) * self.parallel
        else:
            return (
                float(panel.short_circuit_current)
                + (
                    (float(panel.temperature_factor_current) / 1000)
                    * (temp - panel.temperature)
                )
            ) * self.parallel
