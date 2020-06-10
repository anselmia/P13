from django.test import TestCase
from django.urls import reverse
from user.models import User
from design.forms import (
    ProjectForm,
    RoofForm,
    ImplantationForm,
    ConfigForm,
    MPPForm,
)


class DesignTests(TestCase):
    """ Unit Test Class for profil function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(
            username="usertest2",
            password="!!!!!!!!",
            email="test_test@test2.fr",
        )
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.user = User.objects.get(username=self.credentials["username"])

    def test_design_page(self):  # pragma: no cover
        response = self.client.get("/design/")
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        response = self.client.get(reverse("design:index"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "index_design.html")

    def test_project_valid(self):  # pragma: no cover

        form = UserUpdateForm(
            data={"username": "user1", "email": "test@test.fr1"},
            instance=self.user,
        )
        self.assertTrue(form.is_valid())

    def test_UserUpdateForm_invalid_user_exist(self):  # pragma: no cover
        form = UserUpdateForm(
            data={"user_name": "usertest2", "email": "test@test.fr2222"},
            instance=self.user,
        )
        self.assertFalse(form.is_valid())

    def test_UserUpdateForm_invalid_email_exist(self):  # pragma: no cover
        form = UserUpdateForm(
            data={"user_name": "user", "email": "test_test@test2.fr"},
            instance=self.user,
        )
        self.assertFalse(form.is_valid())

    def test_update_profile(self):  # pragma: no cover
        self.client.post(
            reverse("user:profile"),
            {"username": "user2", "email": "test@test.fr2"},
            follow=True,
        )
        # should be logged in now
        self.assertTrue(User.objects.filter(username="user2").exists())
