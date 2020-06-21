""" user App functional Tests """
from user.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create your tests here.


class LoginLiveTestCase(StaticLiveServerTestCase):
    """ Functional Test Class for login function """

    def setUp(self):  # pragma: no cover
        """ setUp of the test """
        self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
        User.objects.create_user(**self.credentials)
        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.selenium = webdriver.Chrome(
            chrome_options=options, executable_path=ChromeDriver
        )
        super(LoginLiveTestCase, self).setUp()

    def tearDown(self):  # pragma: no cover
        """ Tear down of the test """
        self.selenium.quit()
        super(LoginLiveTestCase, self).tearDown()

    def test_login(self):  # pragma: no cover
        """ Simulate login action from webdriver """
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(f"{self.live_server_url}/login/")
        # find the form elements
        username = selenium.find_element_by_id("id_username")
        password = selenium.find_element_by_id("id_password")

        submit = selenium.find_element_by_name("submit")

        # # Fill the form with data
        username.send_keys("testuser")
        password.send_keys("!!!!!!!!")

        # # submitting the form
        submit.send_keys(Keys.RETURN)

        # check the returned result
        selenium.implicitly_wait(5)
        selenium.get(f"{self.live_server_url}")

        assert "Se déconnecter" in selenium.page_source


class LogoutLiveTestCase(StaticLiveServerTestCase):
    """ Functional Test Class for logout function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)

        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
        super(LogoutLiveTestCase, self).setUp()

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

    def tearDown(self):  # pragma: no cover
        """ tearDown of the test """
        self.selenium.quit()
        super(LogoutLiveTestCase, self).tearDown()

    def test_logout(self):  # pragma: no cover
        """ Simulate logout action from webdriver """
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(f"{self.live_server_url}/profile/")
        selenium.maximize_window()
        selenium.implicitly_wait(5)
        logout = selenium.find_element_by_id("logout")
        logout.click()
        selenium.implicitly_wait(5)
        assert "Se connecter" in selenium.page_source
        current_url = selenium.current_url
        if (selenium.current_url[len(selenium.current_url) - 1]) == "/":
            current_url = selenium.current_url[:-1]
        assert current_url == f"{self.live_server_url}"


class RegisterLiveTestCase(StaticLiveServerTestCase):
    """ Functional Test Class for register function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
        super(RegisterLiveTestCase, self).setUp()

    def tearDown(self):  # pragma: no cover
        """ tearDown of the test """
        self.selenium.quit()
        super(RegisterLiveTestCase, self).tearDown()

    def test_register(self):  # pragma: no cover
        """ Simulate register action from webdriver """
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(f"{self.live_server_url}/login/")
        selenium.maximize_window()
        selenium.implicitly_wait(5)

        register = selenium.find_element_by_id("register")
        register.click()
        wait = WebDriverWait(selenium, 20)
        wait.until(EC.visibility_of_element_located((By.ID, "id_robot")))
        selenium.maximize_window()

        username = selenium.find_element_by_id("id_username")
        email = selenium.find_element_by_id("id_email")
        password = selenium.find_element_by_id("id_password1")
        password2 = selenium.find_element_by_id("id_password2")
        robot = selenium.find_element_by_id("id_robot")
        submit = selenium.find_element_by_id("submit")

        i = 0
        while username.get_attribute("value") != "testuser" and i < 10:
            username.click()
            username.clear()
            username.send_keys("testuser")
            i += 1

        email.click()
        email.clear()
        email.send_keys("a@a.fr")
        password.click()
        password.clear()
        password.send_keys("!!!!!!!!")
        password2.click()
        password2.clear()
        password2.send_keys("!!!!!!!!")
        robot.click()
        submit.send_keys(Keys.RETURN)

        wait = WebDriverWait(selenium, 10)
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "about2"))
        )

        current_url = selenium.current_url
        if (selenium.current_url[len(selenium.current_url) - 1]) == "/":
            current_url = selenium.current_url[:-1]
        assert current_url == f"{self.live_server_url}"
        assert "Se déconnecter" in selenium.page_source
        assert User.objects.filter(username="testuser").exists() is True


class ProfileLiveTestCase(StaticLiveServerTestCase):
    """ Functional Test Class for profile function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)

        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
        super(ProfileLiveTestCase, self).setUp()

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

    def tearDown(self):  # pragma: no cover
        """ tearDown of the test """
        self.selenium.quit()
        super(ProfileLiveTestCase, self).tearDown()

    def test_profile(self):  # pragma: no cover
        """ Simulate profile visite action from webdriver """
        selenium = self.selenium
        selenium.get(f"{self.live_server_url}")
        selenium.maximize_window()
        selenium.implicitly_wait(5)

        profile = selenium.find_element_by_id("profile")
        profile.click()
        wait = WebDriverWait(selenium, 20)
        wait.until(
            EC.visibility_of_element_located((By.NAME, "confirm_change"))
        )
        selenium.maximize_window()

        username = selenium.find_element_by_id("id_username")
        submit = selenium.find_element_by_name("confirm_change")
        selenium.execute_script(
            "document.querySelector('button.disabled').removeAttribute('disabled')"
        )
        selenium.execute_script(
            "document.querySelector('button.disabled').classList.remove('disabled')"
        )

        i = 0
        while username.get_attribute("value") != "testuser" and i < 10:
            username.clear()
            username.send_keys("testuser")
            i += 1

        submit.send_keys(Keys.RETURN)
        assert User.objects.filter(username="testuser").exists() is True
