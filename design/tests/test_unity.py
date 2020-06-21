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
from design import api


class DesignTests(TestCase):
    """ Unit Test Class for design function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.user = User.objects.get(username=self.credentials["username"])
        City.objects.create(
            name="test", lat=18.5, lon=18.5,
        )
        Manufacturer.objects.create(name="test",)
        Technology.objects.create(name="test",)
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
        AC_connexion.objects.create(ac_type="Monophasé",)
        AC_connexion.objects.create(ac_type="Triphasé",)
        self.manufacturer = Manufacturer.objects.get(name="test")
        self.ac_connexion = AC_connexion.objects.get(ac_type="Monophasé")
        Inverter.objects.create(
            model="model",
            manufacturer_id=self.manufacturer,
            mpp_voltage_min=1,
            mpp_voltage_max=1,
            dc_voltage_max=1,
            dc_current_max=1,
            dc_power_max=1,
            ac_power_nominal=1,
            ac_power_max=1,
            ac_current_max=1,
            efficiency=1,
            mpp_string_max=1,
            mpp=1,
            ac_cabling=self.ac_connexion,
            comment="comment",
        )

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
            temperature_factor_current=1,
            temperature_factor_current_type=self.temp_current_type,
            temperature_factor_voltage=1,
            temperature_factor_voltage_type=self.temp_voltage_type,
            temperature_factor_power=1,
            temperature_factor_power_type=self.temp_power_type,
            mpp_current=1,
            mpp_voltage=1,
            voltage_max=1,
            length=1,
            width=1,
            serial_cell_quantity=1,
            parallel_cell_quantity=1,
            cell_surface=1,
            comment="comment",
        )
        self.city = City.objects.get(name="test")
        self.panel = Panel.objects.get(model="model")
        Project.objects.create(
            name="test",
            user_id=self.user,
            city_id=self.city,
            panel_id=self.panel,
        )
        self.project = Project.objects.get(name="test")
        self.roof_type = Roof_type.objects.get(value="rectangle")
        Roof.objects.create(
            project_id=self.project,
            roof_type_id=self.roof_type,
            bottom_length=1,
            top_length=1,
            width=1,
            height=1,
            orientation=1,
            tilt=1,
        )
        self.roof = Roof.objects.get(project_id=self.project)
        self.panel_orientation = Orientation.objects.get(value="Paysage")
        self.panel_implantation = Pose.objects.get(value="Côte à côtes")
        Implantation.objects.create(
            roof_id=self.roof,
            panel_orientation=self.panel_orientation,
            panel_implantation=self.panel_implantation,
            vertical_overlapping=1,
            horizontal_overlapping=1,
            vertical_spacing=1,
            horizontal_spacing=1,
            distance_top=1,
            distance_bottom=1,
            distance_left=1,
            distance_right=1,
            abergement_top=1,
            abergement_bottom=1,
            abergement_left=1,
            abergement_right=1,
        )
        self.inverter = Inverter.objects.get(model="model")
        Config.objects.create(
            project_id=self.project,
            inverter_id=self.inverter,
            inverter_quantity=1,
            index=1,
        )
        self.config = Config.objects.get(project_id=self.project)
        MPP.objects.create(
            config_id=self.config, serial=1, parallel=1, index=1,
        )

    def test_design_page(self):  # pragma: no cover
        """ test url design/ """
        response = self.client.get("/design/", follow=True)
        self.assertEquals(response.status_code, 200)

    def test_design_view_project_page(self):  # pragma: no cover
        """ test url design/ """
        response = self.client.get("/design/test/", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.context["form_project"].initial["name"], "test"
        )

    def test_view(self):  # pragma: no cover
        """ test reverse url design:index """
        response = self.client.get(reverse("design:index"), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "index_design.html")

    def test_view_project_page(self):  # pragma: no cover
        """ test url design/ """
        response = self.client.get(
            reverse(
                "design:index_project", kwargs={"project_name": "test"}
            ),
            follow=True,
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.context["form_project"].initial["name"], "test"
        )


class LocalisationTests(TestCase):
    """ Test Class for localisation function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.user = User.objects.get(username=self.credentials["username"])

    def test_localisation_data_page(self):  # pragma: no cover
        """ test url get_localisation_data/ """
        response = self.client.post(
            "/get_localisation_data/", {"search": "Nice"}, follow=True
        )
        self.assertTrue(json.loads(response.content)["status"], True)

    def test_view(self):  # pragma: no cover
        """ test reverse url design:get_localisation_data """
        response = self.client.post(
            reverse("design:get_localisation_data"),
            {"search": "Nice"},
            follow=True,
        )
        self.assertTrue(json.loads(response.content)["status"], True)


class Add_cityTests(TestCase):
    """ Unit Test Class for add_city function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.user = User.objects.get(username=self.credentials["username"])

    def test_add_city_url(self):
        """ test /add_city/ url """
        response = self.client.post(
            "/add_city/",
            data={"name": "test3", "lat": 1, "lon": 1},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["success"], True)

    def test_add_city_error(self):
        """ test /add_city/ url """
        response = self.client.post(
            "/add_city/",
            data={"name": "test3", "lat": 1},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"], True)

    def test_view(self):  # pragma: no cover
        """ test reverse url design:add_city """
        response = self.client.post(
            reverse("design:add_city",),
            data={"name": "test3", "lat": 1, "lon": 1},
            follow=True,
        )
        self.assertTrue(json.loads(response.content)["success"], True)


class Add_panelTests(TestCase):
    """ Unit Test Class for add_panel function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.user = User.objects.get(username=self.credentials["username"])

        Manufacturer.objects.create(name="test",)
        Technology.objects.create(name="test",)

        Temperature_coefficient.objects.create(value="%/°C",)
        Temperature_coefficient.objects.create(value="mA/°C",)
        Temperature_coefficient.objects.create(value="mV/°C",)
        Temperature_coefficient.objects.create(value="mW/°C",)

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

    def test_add_panel_url(self):
        """ test /add_panel/ url """
        response = self.client.post(
            "/add_panel/",
            data={
                "model": "model2",
                "manufacturer_id": self.manufacturer.id,
                "technology_id": self.technology.id,
                "power": 1,
                "tolerance": 1,
                "radiation": 1,
                "temperature": 1,
                "short_circuit_current": 1,
                "open_circuit_voltage": 1,
                "temperature_factor_current": 1,
                "temperature_factor_current_type": self.temp_current_type.id,
                "temperature_factor_voltage": 1,
                "temperature_factor_voltage_type": self.temp_voltage_type.id,
                "temperature_factor_power": 1,
                "temperature_factor_power_type": self.temp_power_type.id,
                "mpp_current": 1,
                "mpp_voltage": 1,
                "voltage_max": 1,
                "length": 1,
                "width": 1,
                "serial_cell_quantity": 1,
                "parallel_cell_quantity": 1,
                "cell_surface": 1,
                "comment": "comment",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["success"], True)

    def test_view(self):  # pragma: no cover
        """ test reverse url design:add_panel """
        response = self.client.post(
            reverse("design:add_panel"),
            data={
                "model": "model2",
                "manufacturer_id": self.manufacturer.id,
                "technology_id": self.technology.id,
                "power": 1,
                "tolerance": 1,
                "radiation": 1,
                "temperature": 1,
                "short_circuit_current": 1,
                "open_circuit_voltage": 1,
                "temperature_factor_current": 1,
                "temperature_factor_current_type": self.temp_current_type.id,
                "temperature_factor_voltage": 1,
                "temperature_factor_voltage_type": self.temp_voltage_type.id,
                "temperature_factor_power": 1,
                "temperature_factor_power_type": self.temp_power_type.id,
                "mpp_current": 1,
                "mpp_voltage": 1,
                "voltage_max": 1,
                "length": 1,
                "width": 1,
                "serial_cell_quantity": 1,
                "parallel_cell_quantity": 1,
                "cell_surface": 1,
                "comment": "comment",
            },
            follow=True,
        )
        self.assertTrue(json.loads(response.content)["success"], True)

    def test_add_panel_error(self):
        """ test /add_panel/ url """
        response = self.client.post(
            reverse("design:add_panel"),
            data={
                "manufacturer_id": self.manufacturer.id,
                "technology_id": self.technology.id,
                "power": 1,
                "tolerance": 1,
                "radiation": 1,
                "temperature": 1,
                "short_circuit_current": 1,
                "open_circuit_voltage": 1,
                "temperature_factor_current": 1,
                "temperature_factor_current_type": self.temp_current_type.id,
                "temperature_factor_voltage": 1,
                "temperature_factor_voltage_type": self.temp_voltage_type.id,
                "temperature_factor_power": 1,
                "temperature_factor_power_type": self.temp_power_type.id,
                "mpp_current": 1,
                "mpp_voltage": 1,
                "voltage_max": 1,
                "length": 1,
                "width": 1,
                "serial_cell_quantity": 1,
                "parallel_cell_quantity": 1,
                "cell_surface": 1,
                "comment": "comment",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"], True)


class Add_inverterTests(TestCase):
    """ Unit Test Class for add_inverter function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.user = User.objects.get(username=self.credentials["username"])

        Manufacturer.objects.create(name="test",)
        AC_connexion.objects.create(ac_type="Monophasé",)
        self.manufacturer = Manufacturer.objects.get(name="test")
        self.ac_connexion = AC_connexion.objects.get(ac_type="Monophasé")

    def test_add_inverter_url(self):
        """ test /add_inverter/ url """
        response = self.client.post(
            "/add_inverter/",
            data={
                "model": "model2",
                "manufacturer_id": self.manufacturer.id,
                "mpp_voltage_min": 1,
                "mpp_voltage_max": 1,
                "dc_voltage_max": 1,
                "dc_current_max": 1,
                "dc_power_max": 1,
                "ac_power_nominal": 1,
                "ac_power_max": 1,
                "ac_current_max": 1,
                "efficiency": 1,
                "mpp_string_max": 1,
                "mpp": 1,
                "ac_cabling": self.ac_connexion.id,
                "comment": "comment",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["success"], True)

    def test_view(self):  # pragma: no cover
        """ test reverse url design:add_inverter """
        response = self.client.post(
            reverse("design:add_inverter",),
            data={
                "model": "model2",
                "manufacturer_id": self.manufacturer.id,
                "mpp_voltage_min": 1,
                "mpp_voltage_max": 1,
                "dc_voltage_max": 1,
                "dc_current_max": 1,
                "dc_power_max": 1,
                "ac_power_nominal": 1,
                "ac_power_max": 1,
                "ac_current_max": 1,
                "efficiency": 1,
                "mpp_string_max": 1,
                "mpp": 1,
                "ac_cabling": self.ac_connexion.id,
                "comment": "comment",
            },
            follow=True,
        )
        self.assertTrue(json.loads(response.content)["success"], True)

    def test_add_inverter_errors(self):  # pragma: no cover
        """ test reverse url design:add_inverter """
        response = self.client.post(
            reverse("design:add_inverter",),
            data={
                "manufacturer_id": self.manufacturer.id,
                "mpp_voltage_min": 1,
                "mpp_voltage_max": 1,
                "dc_voltage_max": 1,
                "dc_current_max": 1,
                "dc_power_max": 1,
                "ac_power_nominal": 1,
                "ac_power_max": 1,
                "ac_current_max": 1,
                "efficiency": 1,
                "mpp_string_max": 1,
                "mpp": 1,
                "ac_cabling": self.ac_connexion.id,
                "comment": "comment",
            },
            follow=True,
        )
        self.assertTrue(json.loads(response.content)["errors"], True)


class ProjectForm(TestCase):
    """ Unit Test Class for project form  """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.user = User.objects.get(username=self.credentials["username"])
        City.objects.create(
            name="test", lat=18.5, lon=18.5,
        )
        Manufacturer.objects.create(name="test",)
        Technology.objects.create(name="test",)

        Temperature_coefficient.objects.create(value="%/°C",)
        Temperature_coefficient.objects.create(value="mA/°C",)
        Temperature_coefficient.objects.create(value="mV/°C",)
        Temperature_coefficient.objects.create(value="mW/°C",)

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
            temperature_factor_current=1,
            temperature_factor_current_type=self.temp_current_type,
            temperature_factor_voltage=1,
            temperature_factor_voltage_type=self.temp_voltage_type,
            temperature_factor_power=1,
            temperature_factor_power_type=self.temp_power_type,
            mpp_current=1,
            mpp_voltage=1,
            voltage_max=1,
            length=1,
            width=1,
            serial_cell_quantity=1,
            parallel_cell_quantity=1,
            cell_surface=1,
            comment="comment",
        )
        self.city = City.objects.get(name="test")
        self.panel = Panel.objects.get(model="model")

    def test_project_valid(self):  # pragma: no cover
        """ test valid project form """
        response = self.client.post(
            "/valid_project/",
            data={
                "name": "test",
                "city_id": self.city.id,
                "panel_id": self.panel.id,
                "user_id": self.user.id,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["success"])

    def test_project_invalid(self):  # pragma: no cover
        """ test invalid project form """
        response = self.client.post(
            "/valid_project/",
            data={"city_id": self.city.id, "panel_id": self.panel.id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])

    def test_save_project_valid(self):  # pragma: no cover
        """ test valid save project form """
        response = self.client.post(
            "/save_project/",
            data={
                "name": "test",
                "city_id": self.city.id,
                "panel_id": self.panel.id,
                "user_id": self.user.id,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["success"])

    def test_save_project_invalid(self):  # pragma: no cover
        """ test invalid save project form """
        response = self.client.post(
            "/save_project/",
            data={"city_id": self.city.id, "panel_id": self.panel.id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])


class RoofForm(TestCase):
    """ Unit Test Class for roof form  """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.user = User.objects.get(username=self.credentials["username"])
        City.objects.create(
            name="test", lat=18.5, lon=18.5,
        )
        Manufacturer.objects.create(name="test",)
        Technology.objects.create(name="test",)
        Roof_type.objects.create(value="rectangle",)
        Roof_type.objects.create(value="trapèze",)
        Roof_type.objects.create(value="triangle",)
        self.manufacturer = Manufacturer.objects.get(name="test")
        self.technology = Technology.objects.get(name="test")
        Temperature_coefficient.objects.create(value="%/°C",)
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
            temperature_factor_current=1,
            temperature_factor_current_type=self.temp_current_type,
            temperature_factor_voltage=1,
            temperature_factor_voltage_type=self.temp_voltage_type,
            temperature_factor_power=1,
            temperature_factor_power_type=self.temp_power_type,
            mpp_current=1,
            mpp_voltage=1,
            voltage_max=1,
            length=1,
            width=1,
            serial_cell_quantity=1,
            parallel_cell_quantity=1,
            cell_surface=1,
            comment="comment",
        )
        self.city = City.objects.get(name="test")
        self.panel = Panel.objects.get(model="model")
        Project.objects.create(
            name="test",
            user_id=self.user,
            city_id=self.city,
            panel_id=self.panel,
        )
        self.project = Project.objects.get(name="test")
        self.roof_type1 = Roof_type.objects.get(value="rectangle")
        self.roof_type2 = Roof_type.objects.get(value="trapèze")
        self.roof_type3 = Roof_type.objects.get(value="triangle")
        session = self.client.session
        session["project_id"] = self.project.id
        session["panel_id"] = self.panel.id
        session.save()

    def test_roof_valid(self):  # pragma: no cover
        """ test valid roof form """
        response = self.client.post(
            "/valid_roof/",
            data={
                "project_id": self.project.id,
                "roof_type_id": self.roof_type1.id,
                "bottom_length": 1,
                "top_length": 1,
                "width": 1,
                "height": 1,
                "orientation": 1,
                "tilt": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["success"])

    def test_roof_invalid(self):  # pragma: no cover
        """ test invalid roof form """
        response = self.client.post(
            "/valid_roof/",
            data={
                "project_id": self.project.id,
                "bottom_length": 1,
                "top_length": 1,
                "width": 1,
                "height": 1,
                "orientation": 1,
                "tilt": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])

    def test_roof_invalid1(self):  # pragma: no cover
        """ test invalid roof form """
        response = self.client.post(
            "/valid_roof/",
            data={
                "project_id": self.project.id,
                "roof_type_id": self.roof_type1.id,
                "bottom_length": 0,
                "top_length": 0,
                "width": 0,
                "height": 0,
                "orientation": 1,
                "tilt": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])

    def test_roof_invalid2(self):  # pragma: no cover
        """ test invalid roof form """
        response = self.client.post(
            "/valid_roof/",
            data={
                "project_id": self.project.id,
                "roof_type_id": self.roof_type2.id,
                "bottom_length": 5,
                "top_length": 7,
                "width": 1,
                "height": 1,
                "orientation": 1,
                "tilt": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])

    def test_roof_invalid3(self):  # pragma: no cover
        """ test invalid roof form """
        response = self.client.post(
            "/valid_roof/",
            data={
                "project_id": self.project.id,
                "roof_type_id": self.roof_type3.id,
                "bottom_length": 5,
                "top_length": 1,
                "width": 2,
                "height": 1,
                "orientation": 1,
                "tilt": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])

    def test_save_roof_valid(self):  # pragma: no cover
        """ test valid save roof form """
        response = self.client.post(
            "/save_roof/",
            data={
                "project_id": self.project.id,
                "roof_type_id": self.roof_type1.id,
                "bottom_length": 1,
                "top_length": 1,
                "width": 1,
                "height": 1,
                "orientation": 1,
                "tilt": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["success"])

    def test_save_roof_invalid(self):  # pragma: no cover
        """ test invalid save roof form """
        response = self.client.post(
            "/save_roof/",
            data={
                "project_id": self.project.id,
                "bottom_length": 1,
                "top_length": 1,
                "width": 1,
                "height": 1,
                "orientation": 1,
                "tilt": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])


class ImplantationForm(TestCase):
    """ Unit Test Class for implantation form  """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.user = User.objects.get(username=self.credentials["username"])
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
            temperature_factor_current=1,
            temperature_factor_current_type=self.temp_current_type,
            temperature_factor_voltage=1,
            temperature_factor_voltage_type=self.temp_voltage_type,
            temperature_factor_power=1,
            temperature_factor_power_type=self.temp_power_type,
            mpp_current=1,
            mpp_voltage=1,
            voltage_max=1,
            length=1,
            width=1,
            serial_cell_quantity=1,
            parallel_cell_quantity=1,
            cell_surface=1,
            comment="comment",
        )
        self.city = City.objects.get(name="test")
        self.panel = Panel.objects.get(model="model")
        Project.objects.create(
            name="test",
            user_id=self.user,
            city_id=self.city,
            panel_id=self.panel,
        )
        self.project = Project.objects.get(name="test")
        self.roof_type = Roof_type.objects.get(value="rectangle")
        Roof.objects.create(
            project_id=self.project,
            roof_type_id=self.roof_type,
            bottom_length=1,
            top_length=1,
            width=1,
            height=1,
            orientation=1,
            tilt=1,
        )
        self.roof = Roof.objects.get(project_id=self.project)
        self.panel_orientation = Orientation.objects.get(value="Paysage")
        self.panel_implantation = Pose.objects.get(value="Côte à côtes")
        self.panel_implantation2 = Pose.objects.get(value="Espacés")
        self.panel_implantation3 = Pose.objects.get(value="Recouverts")
        session = self.client.session
        session["roof_id"] = self.roof.id
        session.save()

    def test_implantation_valid(self):  # pragma: no cover
        """ test valid implantation form """
        response = self.client.post(
            "/valid_implantation/",
            {
                "panel_orientation": self.panel_orientation.id,
                "panel_implantation": self.panel_implantation.id,
                "vertical_overlapping": 1,
                "horizontal_overlapping": 1,
                "vertical_spacing": 1,
                "horizontal_spacing": 1,
                "distance_top": 1,
                "distance_bottom": 1,
                "distance_left": 1,
                "distance_right": 1,
                "abergement_top": 1,
                "abergement_bottom": 1,
                "abergement_left": 1,
                "abergement_right": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["success"])

    def test_implantation_invalid(self):  # pragma: no cover
        """ test invalid implantation form """
        response = self.client.post(
            "/valid_implantation/",
            data={
                "panel_implantation": self.panel_implantation.id,
                "vertical_overlapping": 1,
                "horizontal_overlapping": 1,
                "vertical_spacing": 1,
                "horizontal_spacing": 1,
                "distance_top": 1,
                "distance_bottom": 1,
                "distance_left": 1,
                "distance_right": 1,
                "abergement_top": 1,
                "abergement_bottom": 1,
                "abergement_left": 1,
                "abergement_right": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])

    def test_implantation_invalid2(self):  # pragma: no cover
        """ test invalid implantation form """
        response = self.client.post(
            "/valid_implantation/",
            data={
                "panel_implantation": self.panel_implantation2.id,
                "vertical_overlapping": 1,
                "horizontal_overlapping": 1,
                "vertical_spacing": -1,
                "horizontal_spacing": -1,
                "distance_top": 1,
                "distance_bottom": 1,
                "distance_left": 1,
                "distance_right": 1,
                "abergement_top": 1,
                "abergement_bottom": 1,
                "abergement_left": 1,
                "abergement_right": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])

    def test_implantation_invalid3(self):  # pragma: no cover
        """ test invalid implantation form """
        response = self.client.post(
            "/valid_implantation/",
            data={
                "panel_implantation": self.panel_implantation3.id,
                "vertical_overlapping": -1,
                "horizontal_overlapping": -1,
                "vertical_spacing": 1,
                "horizontal_spacing": 1,
                "distance_top": 1,
                "distance_bottom": 1,
                "distance_left": 1,
                "distance_right": 1,
                "abergement_top": 1,
                "abergement_bottom": 1,
                "abergement_left": 1,
                "abergement_right": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])

    def test_save_implantation_valid(self):  # pragma: no cover
        """ test valid save implantation form """
        response = self.client.post(
            "/save_implantation/",
            data={
                "panel_orientation": self.panel_orientation.id,
                "panel_implantation": self.panel_implantation.id,
                "vertical_overlapping": 1,
                "horizontal_overlapping": 1,
                "vertical_spacing": 1,
                "horizontal_spacing": 1,
                "distance_top": 1,
                "distance_bottom": 1,
                "distance_left": 1,
                "distance_right": 1,
                "abergement_top": 1,
                "abergement_bottom": 1,
                "abergement_left": 1,
                "abergement_right": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["success"])

    def test_save_implantation_invalid(self):  # pragma: no cover
        """ test invalid save implantation form """
        response = self.client.post(
            "/save_implantation/",
            data={
                "panel_implantation": self.panel_implantation.id,
                "vertical_overlapping": 1,
                "horizontal_overlapping": 1,
                "vertical_spacing": 1,
                "horizontal_spacing": 1,
                "distance_top": 1,
                "distance_bottom": 1,
                "distance_left": 1,
                "distance_right": 1,
                "abergement_top": 1,
                "abergement_bottom": 1,
                "abergement_left": 1,
                "abergement_right": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])


class ConfigurationForm(TestCase):
    """ Unit Test Class for Configuration form  """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.user = User.objects.get(username=self.credentials["username"])
        City.objects.create(
            name="test", lat=18.5, lon=18.5,
        )
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
            temperature_factor_current=1,
            temperature_factor_current_type=self.temp_current_type,
            temperature_factor_voltage=1,
            temperature_factor_voltage_type=self.temp_voltage_type,
            temperature_factor_power=1,
            temperature_factor_power_type=self.temp_power_type,
            mpp_current=1,
            mpp_voltage=1,
            voltage_max=1,
            length=1,
            width=1,
            serial_cell_quantity=1,
            parallel_cell_quantity=1,
            cell_surface=1,
            comment="comment",
        )
        self.city = City.objects.get(name="test")
        self.panel = Panel.objects.get(model="model")
        Project.objects.create(
            name="test",
            user_id=self.user,
            city_id=self.city,
            panel_id=self.panel,
        )
        self.project = Project.objects.get(name="test")
        AC_connexion.objects.create(ac_type="Monophasé",)
        AC_connexion.objects.create(ac_type="Triphasé",)
        self.manufacturer = Manufacturer.objects.get(name="test")
        self.ac_connexion = AC_connexion.objects.get(ac_type="Monophasé")
        Inverter.objects.create(
            model="model",
            manufacturer_id=self.manufacturer,
            mpp_voltage_min=1,
            mpp_voltage_max=1,
            dc_voltage_max=1,
            dc_current_max=1,
            dc_power_max=1,
            ac_power_nominal=1,
            ac_power_max=1,
            ac_current_max=1,
            efficiency=1,
            mpp_string_max=1,
            mpp=1,
            ac_cabling=self.ac_connexion,
            comment="comment",
        )
        self.inverter = Inverter.objects.get(model="model")

        session = self.client.session
        session["project_id"] = self.project.id
        session.save()

    def test_configuration_valid(self):  # pragma: no cover
        """ test valid configuration form """
        response = self.client.post(
            "/valid_configuration/",
            data={
                "inverter_id": self.inverter.id,
                "inverter_quantity": 1,
                "index": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["success"])

    def test_configuration_invalid(self):  # pragma: no cover
        """ test invalid configuration form """
        response = self.client.post(
            "/valid_configuration/",
            data={"inverter_quantity": 1, "index": 1},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])

    def test_save_configuration_valid(self):  # pragma: no cover
        """ test valid save configuration form """
        response = self.client.post(
            "/save_configuration/",
            data={
                "inverter_id": self.inverter.id,
                "inverter_quantity": 1,
                "index": 1,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["success"])

    def test_save_configuration_invalid(self):  # pragma: no cover
        """ test invalid save configuration form """
        response = self.client.post(
            "/save_configuration/",
            data={"inverter_quantity": 1, "index": 1},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])


class MPPForm(TestCase):
    """ Unit Test Class for MPP form  """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.user = User.objects.get(username=self.credentials["username"])
        City.objects.create(
            name="test", lat=18.5, lon=18.5,
        )
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
            temperature_factor_current=1,
            temperature_factor_current_type=self.temp_current_type,
            temperature_factor_voltage=1,
            temperature_factor_voltage_type=self.temp_voltage_type,
            temperature_factor_power=1,
            temperature_factor_power_type=self.temp_power_type,
            mpp_current=1,
            mpp_voltage=1,
            voltage_max=1,
            length=1,
            width=1,
            serial_cell_quantity=1,
            parallel_cell_quantity=1,
            cell_surface=1,
            comment="comment",
        )
        self.city = City.objects.get(name="test")
        self.panel = Panel.objects.get(model="model")
        Project.objects.create(
            name="test",
            user_id=self.user,
            city_id=self.city,
            panel_id=self.panel,
        )
        self.project = Project.objects.get(name="test")
        AC_connexion.objects.create(ac_type="Monophasé",)
        AC_connexion.objects.create(ac_type="Triphasé",)
        self.manufacturer = Manufacturer.objects.get(name="test")
        self.ac_connexion = AC_connexion.objects.get(ac_type="Monophasé")
        Inverter.objects.create(
            model="model",
            manufacturer_id=self.manufacturer,
            mpp_voltage_min=1,
            mpp_voltage_max=1,
            dc_voltage_max=1,
            dc_current_max=1,
            dc_power_max=1,
            ac_power_nominal=1,
            ac_power_max=1,
            ac_current_max=1,
            efficiency=1,
            mpp_string_max=1,
            mpp=1,
            ac_cabling=self.ac_connexion,
            comment="comment",
        )
        self.inverter = Inverter.objects.get(model="model")
        Config.objects.create(
            project_id=self.project,
            inverter_id=self.inverter,
            inverter_quantity=1,
            index=1,
        )
        self.config = Config.objects.get(project_id=self.project)

        session = self.client.session
        session["config_id"] = self.config.id
        session.save()

    def test_mpp_valid(self):  # pragma: no cover
        """ test valid mpp form """
        response = self.client.post(
            "/valid_mpp/",
            data={"serial": 1, "parallel": 1, "index": 1},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["success"])

    def test_mpp_invalid(self):  # pragma: no cover
        """ test invalid mpp form """
        response = self.client.post(
            "/valid_mpp/",
            data={"serial": 1, "parallel": 1},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])

    def test_save_mpp_valid(self):  # pragma: no cover
        """ test valid save mpp form """
        response = self.client.post(
            "/save_mpp/",
            data={"serial": 1, "parallel": 1, "index": 1},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["success"])

    def test_save_mpp_invalid(self):  # pragma: no cover
        """ test invalid save mpp form """
        response = self.client.post(
            "/save_mpp/",
            data={"serial": 1, "parallel": 1},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTrue(json.loads(response.content)["errors"])


class CalculImplantation(TestCase):
    """ Class to test calculation related to implantation """

    def setUp(self):
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.user = User.objects.get(username=self.credentials["username"])
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
            temperature_factor_current=1,
            temperature_factor_current_type=self.temp_current_type,
            temperature_factor_voltage=1,
            temperature_factor_voltage_type=self.temp_voltage_type,
            temperature_factor_power=1,
            temperature_factor_power_type=self.temp_power_type,
            mpp_current=1,
            mpp_voltage=1,
            voltage_max=1,
            length=1000,
            width=1000,
            serial_cell_quantity=1,
            parallel_cell_quantity=1,
            cell_surface=1,
            comment="comment",
        )
        self.panel = Panel.objects.get(model="model")
        self.roof_type1 = Roof_type.objects.get(value="rectangle")
        self.roof_type2 = Roof_type.objects.get(value="trapèze")
        self.roof_type3 = Roof_type.objects.get(value="triangle")
        self.panel_implantation1 = Pose.objects.get(value="Côte à côtes")
        self.panel_implantation2 = Pose.objects.get(value="Espacés")
        self.panel_implantation3 = Pose.objects.get(value="Recouverts")
        self.panel_orientation1 = Orientation.objects.get(value="Paysage")
        self.panel_orientation2 = Orientation.objects.get(value="Portrait")

        self.data = {
            "panel_id": self.panel.id,
            "bottom_length": 1,
            "top_length": 1,
            "width": 1,
            "height": 1,
            "orientation": 1,
            "tilt": 1,
            "vertical_overlapping": 100,
            "horizontal_overlapping": 100,
            "vertical_spacing": 100,
            "horizontal_spacing": 100,
            "distance_top": 1,
            "distance_bottom": 1,
            "distance_left": 1,
            "distance_right": 1,
            "abergement_top": 100,
            "abergement_bottom": 100,
            "abergement_left": 100,
            "abergement_right": 100,
        }

    def test_calculation_implantation(self):
        """ Test implantation covering """
        roof_types = [self.roof_type1, self.roof_type2, self.roof_type3]
        orientations = [self.panel_orientation1, self.panel_orientation2]
        implantations = [
            self.panel_implantation1,
            self.panel_implantation2,
            self.panel_implantation3,
        ]
        success = 0
        for roof_type in roof_types:
            for orientation in orientations:
                for implantation in implantations:
                    self.data["roof_type_id"] = roof_type.id
                    self.data["panel_orientation"] = orientation.id
                    self.data["panel_implantation"] = implantation.id

                    if roof_type.value == "rectangle":
                        self.data["bottom_length"] = 5
                        self.data["top_length"] = 0
                        self.data["width"] = 5
                        self.data["height"] = 0
                    elif roof_type.value == "trapèze":
                        self.data["bottom_length"] = 10
                        self.data["top_length"] = 6
                        self.data["width"] = 0
                        self.data["height"] = 4
                    elif roof_type.value == "triangle":
                        self.data["bottom_length"] = 10
                        self.data["top_length"] = 0
                        self.data["width"] = 6
                        self.data["height"] = 0

                    response = self.client.post(
                        "/calcul_implantation/",
                        self.data,
                        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
                    )
                    try:
                        if json.loads(response.content)["success"]:
                            success += 1
                    except Exception:
                        pass

        self.assertTrue(success == 18)


class Informations(TestCase):
    """ Class to test informations file """

    def setUp(self):
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.user = User.objects.get(username=self.credentials["username"])
        City.objects.create(
            name="test", lat=18.5, lon=18.5,
        )
        self.site = City.objects.get(name="test")
        Manufacturer.objects.create(name="test",)
        self.manufacturer = Manufacturer.objects.get(name="test")
        Temperature_coefficient.objects.create(value="%/°C",)
        Temperature_coefficient.objects.create(value="mA/°C",)
        Temperature_coefficient.objects.create(value="mV/°C",)
        Temperature_coefficient.objects.create(value="mW/°C",)
        Technology.objects.create(name="test",)
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
            temperature_factor_current=1,
            temperature_factor_current_type=self.temp_current_type,
            temperature_factor_voltage=1,
            temperature_factor_voltage_type=self.temp_voltage_type,
            temperature_factor_power=1,
            temperature_factor_power_type=self.temp_power_type,
            mpp_current=1,
            mpp_voltage=1,
            voltage_max=1,
            length=1000,
            width=1000,
            serial_cell_quantity=1,
            parallel_cell_quantity=1,
            cell_surface=1,
            comment="comment",
        )
        self.panel = Panel.objects.get(model="model")
        Project.objects.create(
            name="test",
            user_id=self.user,
            city_id=self.site,
            panel_id=self.panel,
        )
        self.project = Project.objects.get(name="test")
        AC_connexion.objects.create(ac_type="Monophasé",)
        AC_connexion.objects.create(ac_type="Triphasé",)
        self.ac_connexion = AC_connexion.objects.get(ac_type="Monophasé")
        Inverter.objects.create(
            model="model",
            manufacturer_id=self.manufacturer,
            mpp_voltage_min=1,
            mpp_voltage_max=1,
            dc_voltage_max=1,
            dc_current_max=1,
            dc_power_max=1,
            ac_power_nominal=1,
            ac_power_max=1,
            ac_current_max=1,
            efficiency=1,
            mpp_string_max=1,
            mpp=1,
            ac_cabling=self.ac_connexion,
            comment="comment",
        )
        self.inverter = Inverter.objects.get(model="model")
        Config.objects.create(
            project_id=self.project,
            inverter_id=self.inverter,
            inverter_quantity=1,
            index=1,
        )
        self.config = Config.objects.get(project_id=self.project)

    def test_production_information(self):
        """ Test production informations """
        datas = {
            "config": [
                {
                    "index": 1,
                    "inverter_id": str(self.inverter.id),
                    "inverter_quantity": "6",
                    "mpps": [
                        {"index": 1, "parallel": "1", "serial": "11"}
                    ],
                }
            ],
            "panel_id": str(self.panel.id),
            "site_id": str(self.site.id),
            "tot_pan": "10",
        }
        datas = {"data": json.dumps(datas)}
        response = self.client.post(
            "/production_data/",
            datas,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        value_to_return = {
            "pv_data": [
                self.panel.model,
                self.panel.power,
                self.panel.length * self.panel.width * 10 / 1000000,
            ],
            "site_data": [
                self.site.name,
                float(self.site.lat),
                float(self.site.lon),
            ],
            "inverters_datas": [[0, self.inverter.model, "1.00",]],
        }
        print(response.json()["infos"])
        print(response.json()["infos"])
        print(value_to_return)
        self.assertTrue(response.json()["infos"] == value_to_return)

