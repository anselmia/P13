""" design App functional Tests """

import time
from user.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import json
from django.test import TestCase
from django.urls import reverse
from user.models import User
from design.models import (
    Project,
    City,
    Roof,
    Implantation,
    Config,
    MPP,
    Manufacturer,
    Technology,
    Roof_type,
    Orientation,
    Pose,
    Temperature_coefficient,
    AC_connexion,
    Inverter,
    Panel,
)
from design.forms import (
    ProjectForm,
    CityForm,
    RoofForm,
    ImplantationForm,
    ConfigForm,
    MPPForm,
    PanelForm,
    InverterForm,
)
from django.test.client import Client
from design.implantation_calculation import Implantation_calculation

# Create your tests here.


class DesignLiveTestCase(StaticLiveServerTestCase):
    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.user = User.objects.get(username=self.credentials["username"])
        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
        super(DesignLiveTestCase, self).setUp()

        # Login the user
        self.assertTrue(
            self.client.login(
                username=self.credentials["username"],
                password=self.credentials["password"],
            )
        )
        # Add cookie to log in the browser
        cookie = self.client.cookies["sessionid"]
        self.selenium.get(
            self.live_server_url
        )  # visit page in the site domain so the page accepts the cookie
        self.selenium.add_cookie(
            {
                "name": "sessionid",
                "value": cookie.value,
                "secure": False,
                "path": "/",
            }
        )

        City.objects.create(
            name="test", lat=18.5, lon=18.5,
        )
        Roof_type.objects.create(value="rectangle",)
        Roof_type.objects.create(value="trapèze",)
        Roof_type.objects.create(value="triangle",)
        Orientation.objects.create(value="Paysage",)
        Orientation.objects.create(value="Portrait",)
        Pose.objects.create(value="Côte à côtes",)
        Pose.objects.create(value="Espacés",)
        Pose.objects.create(value="Recouverts",)
        Temperature_coefficient.objects.create(value="%/°C",)
        Temperature_coefficient.objects.create(value="mA/°C",)
        Temperature_coefficient.objects.create(value="mV/°C",)
        Temperature_coefficient.objects.create(value="mW/°C",)
        Manufacturer.objects.create(name="test",)
        Technology.objects.create(name="test",)
        self.manufacturer = Manufacturer.objects.get(name="test")
        self.technology = Technology.objects.get(name="test")
        self.temp_current_type = Temperature_coefficient.objects.get(
            value="%/°C"
        )
        self.temp_voltage_type = Temperature_coefficient.objects.get(
            value="%/°C"
        )
        self.temp_power_type = Temperature_coefficient.objects.get(
            value="%/°C"
        )

        Panel.objects.create(
            model="model",
            manufacturer_id=self.manufacturer,
            technology_id=self.technology,
            power=1,
            tolerance=1,
            radiation=1,
            temperature=1,
            short_circuit_current=1,
            open_circuit_voltage=1,
            temperature_factor_current=0.001,
            temperature_factor_current_type=self.temp_current_type,
            temperature_factor_voltage=0.001,
            temperature_factor_voltage_type=self.temp_voltage_type,
            temperature_factor_power=0.001,
            temperature_factor_power_type=self.temp_power_type,
            mpp_current=1,
            mpp_voltage=1,
            voltage_max=1000,
            length=1000,
            width=1000,
            serial_cell_quantity=1,
            parallel_cell_quantity=1,
            cell_surface=1,
            comment="comment",
        )
        self.city = City.objects.get(name="test")
        self.panel = Panel.objects.get(model="model")
        self.roof_type1 = Roof_type.objects.get(value="rectangle")
        self.roof_type2 = Roof_type.objects.get(value="trapèze")
        self.roof_type3 = Roof_type.objects.get(value="triangle")
        self.panel_implantation1 = Pose.objects.get(value="Côte à côtes")
        self.panel_implantation2 = Pose.objects.get(value="Espacés")
        self.panel_implantation3 = Pose.objects.get(value="Recouverts")
        self.panel_orientation1 = Orientation.objects.get(value="Paysage")
        self.panel_orientation2 = Orientation.objects.get(value="Portrait")

        AC_connexion.objects.create(ac_type="Monophasé",)
        AC_connexion.objects.create(ac_type="Triphasé",)
        self.ac_connexion = AC_connexion.objects.get(ac_type="Monophasé")
        Inverter.objects.create(
            model="model",
            manufacturer_id=self.manufacturer,
            mpp_voltage_min=1,
            mpp_voltage_max=1000,
            dc_voltage_max=1000,
            dc_current_max=30,
            dc_power_max=1,
            ac_power_nominal=1,
            ac_power_max=1,
            ac_current_max=30,
            efficiency=80,
            mpp_string_max=3,
            mpp=3,
            ac_cabling=self.ac_connexion,
            comment="comment",
        )

    def tearDown(self):  # pragma: no cover
        """ tearDown of the test """
        self.selenium.quit()
        super(DesignLiveTestCase, self).tearDown()

    def test_design_rooftype_1(self):  # pragma: no cover
        """ Simulate design action from webdriver """
        selenium = self.selenium

        selenium.get(f"{self.live_server_url}/design/")
        selenium.maximize_window()
        selenium.implicitly_wait(5)

        bt_next = selenium.find_element_by_class_name("sw-btn-next")
        project_name = selenium.find_element_by_id("id_name")

        city = selenium.find_element_by_id("id_city_id")
        option = None
        for opt in city.find_elements_by_tag_name("option"):
            if opt.text == "test":
                option = opt

        option.click()

        panel = selenium.find_element_by_id("id_panel_id")
        for opt in panel.find_elements_by_tag_name("option"):
            if opt.text == "model":
                option = opt

        option.click()

        project_name.click()
        project_name.clear()
        project_name.send_keys("test")

        time.sleep(1)
        bt_next.click()
        wait = WebDriverWait(selenium, 20)
        wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "form_roof"))
        )

        roof_type = selenium.find_element_by_id("id_roof_type_id")
        for opt in roof_type.find_elements_by_tag_name("option"):
            if opt.text == "rectangle":
                option = opt

        option.click()

        width = selenium.find_element_by_id("id_width")
        length = selenium.find_element_by_id("id_bottom_length")

        width.click()
        width.clear()
        width.send_keys(10)

        length.click()
        length.clear()
        length.send_keys(10)
        time.sleep(1)

        bt_next.click()
        time.sleep(1)
        panel_orientation = selenium.find_element_by_id(
            "id_panel_orientation"
        )
        for opt in panel_orientation.find_elements_by_tag_name("option"):
            if opt.text == "Paysage":
                option = opt

        option.click()

        panel_implantation = selenium.find_element_by_id(
            "id_panel_implantation"
        )
        for opt in panel_implantation.find_elements_by_tag_name("option"):
            if opt.text == "Côte à côtes":
                option = opt

        option.click()

        bt_draw = selenium.find_element_by_class_name("draw")
        bt_draw.click()
        time.sleep(4)
        bt_next.click()
        time.sleep(1)

        inverter = selenium.find_element_by_id("id_inverter_id")
        for opt in inverter.find_elements_by_tag_name("option"):
            if opt.text == "model":
                option = opt

        option.click()

        quantity = selenium.find_element_by_id("id_inverter_quantity")
        serial = selenium.find_element_by_id("id_serial")
        parallel = selenium.find_element_by_id("id_parallel")

        quantity.click()
        quantity.clear()
        quantity.send_keys(10)
        time.sleep(1)

        serial.click()
        serial.clear()
        serial.send_keys(10)
        time.sleep(1)

        parallel.click()
        parallel.clear()
        parallel.send_keys(1)

        serial.click()

        time.sleep(2)
        bt_next.click()
        time.sleep(2)

        irrad = selenium.find_element_by_xpath(
            "//p[contains(@class, 'energy_irrad_year')]"
        ).text
        irrad = int(irrad)

        save_prod = selenium.find_element_by_class_name("save_prod")
        save_prod.click()

        time.sleep(2)

        assert irrad > 0
        assert len(MPP.objects.all()) > 0

        myproject = selenium.find_element_by_id("project")
        myproject.click()

        time.sleep(2)
        project = selenium.find_element_by_xpath(
            "//a[contains(@name, 'test')]"
        )
        project.click()
        time.sleep(3)
        project_name = selenium.find_element_by_id("id_name")
        print(project_name.get_attribute("value"))
        assert "test" == project_name.get_attribute("value")
