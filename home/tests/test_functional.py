""" home App functional Tests """

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

# Create your tests here.


class HomeLiveTestCase(StaticLiveServerTestCase):
    """ Functional Test of Home page"""

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
        super(HomeLiveTestCase, self).setUp()

    def tearDown(self):  # pragma: no cover
        """ tearDown of the test """
        self.selenium.quit()
        super(HomeLiveTestCase, self).tearDown()

    def test_home(self):  # pragma: no cover
        """ Simulate visit of home page from webdriver """
        selenium = self.selenium

        selenium.get(f"{self.live_server_url}/")
        selenium.maximize_window()
        selenium.implicitly_wait(3)

        assert "photon" in selenium.page_source


class MentionsLiveTestCase(StaticLiveServerTestCase):
    """ Functional Test of Mentions page"""

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
        super(MentionsLiveTestCase, self).setUp()

    def tearDown(self):  # pragma: no cover
        """ tearDown of the test """
        self.selenium.quit()
        super(MentionsLiveTestCase, self).tearDown()

    def test_mentions(self):  # pragma: no cover
        """ Simulate visit of mentions page from webdriver """
        selenium = self.selenium

        selenium.get(f"{self.live_server_url}/")
        selenium.maximize_window()
        selenium.implicitly_wait(3)

        mentions = selenium.find_element_by_id("mentions")
        mentions.click()

        assert "Mention légale" in selenium.page_source
