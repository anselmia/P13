from django.test import TestCase
from django.urls import reverse


class HomeTests(TestCase):
    """ Unit Test Class for home page """

    def test_home_page(self):  # pragma: no cover
        """ test url design/ """
        response = self.client.get("/", follow=True)
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        """ test reverse url home:index """
        response = self.client.get(reverse("home:index"), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class MentionsTests(TestCase):
    """ Unit Test Class for mentions pages """

    def test_mentions_page(self):  # pragma: no cover
        """ test url design/ """
        response = self.client.get("/mentions/", follow=True)
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        """ test reverse url home:mentions """
        response = self.client.get(reverse("home:mentions"), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "mentions.html")
