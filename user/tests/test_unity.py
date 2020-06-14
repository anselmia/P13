from django.test import TestCase
from django.urls import reverse
from user.models import User
from user.forms import ConnexionForm, SignUpForm, UserUpdateForm


class LoginTests(TestCase):
    """ Unit Test Class for login function """

    def setUp(self):  # pragma: no cover
        """ Set Up of the test """
        self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
        User.objects.create_user(**self.credentials)

    def test_login_page(self):  # pragma: no cover
        response = self.client.get("/login/")
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        response = self.client.get(reverse("user:login"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_UserForm_valid(self):  # pragma: no cover
        form = ConnexionForm(
            data={"username": "testuser", "password": "!!!!!!!!"}
        )
        self.assertTrue(form.is_valid())

    def test_UserForm_invalid(self):  # pragma: no cover
        form = ConnexionForm(data={"username": "user"})
        self.assertFalse(form.is_valid())

    def test_invalid_login(self):  # pragma: no cover
        response = self.client.post(
            reverse("user:login"),
            {"username": "testuser", "password": "!!!!!aaa"},
            follow=True,
        )
        self.assertFalse(response.context["user"].is_authenticated)

    def test_login(self):  # pragma: no cover
        response = self.client.post(
            reverse("user:login"), self.credentials, follow=True
        )
        self.assertTrue(response.context["user"].is_authenticated)

    def test_already_login(self):  # pragma: no cover
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        self.client.post(
            reverse("user:login"), self.credentials, follow=True
        )
        self.assertTemplateUsed("home.html")


class LogoutTests(TestCase):
    """ Unit Test Class for logout function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
        User.objects.create_user(**self.credentials)

    def test_logout_page(self):  # pragma: no cover
        """ Test of logout view using verbal url """
        response = self.client.get("logout/")
        self.assertEquals(response.status_code, 404)

    def test_view(self):  # pragma: no cover
        """
        Test of logout view using reverse url
        """
        self.client.login(
            username=self.credentials["username"],
            password=self.credentials["password"],
        )
        response = self.client.get(reverse("user:logout"))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("home:index"))


class RegisterTests(TestCase):
    """ Unit Test Class for register function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "email": "test_test@test.fr",
            "password": "!!!!!!!!",
        }

    def test_register_page(self):  # pragma: no cover
        response = self.client.get("/register/")
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        response = self.client.get(reverse("user:register"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_SignUpForm_valid(self):  # pragma: no cover
        form = SignUpForm(
            data={
                "username": "user1",
                "email": "test@test.fr1",
                "password1": "!!!!!!!!",
                "password2": "!!!!!!!!",
                "robot": True,
            }
        )
        self.assertTrue(form.is_valid())

    def test_SignUpForm_different_password(self):  # pragma: no cover
        form = SignUpForm(
            data={
                "username": "user",
                "email": "test@test.fr",
                "password1": "!!!!!!!!",
                "password2": "!!!!!!!a",
                "robot": True,
            }
        )
        self.assertFalse(form.is_valid())

    def test_SignUpForm_invalid_password(self):  # pragma: no cover
        form = SignUpForm(
            data={
                "username": "user",
                "email": "test@test.fr",
                "password1": "aaaaaaaa",
                "password2": "aaaaaaaa",
                "robot": True,
            }
        )
        self.assertFalse(form.is_valid())

    def test_SignUpForm_user_exist(self):  # pragma: no cover
        User.objects.create_user(**self.credentials)
        form = SignUpForm(
            data={
                "username": "usertest",
                "email": "test_test@test.f",
                "password1": "!!!!!!!!",
                "password2": "!!!!!!!!",
                "robot": True,
            }
        )
        self.assertFalse(form.is_valid())

    def test_register(self):  # pragma: no cover
        self.client.post(
            reverse("user:register"),
            {
                "username": "user2",
                "email": "test@test.fr2",
                "password1": "!!!!!!!!",
                "password2": "!!!!!!!!",
                "robot": True,
            },
            follow=True,
        )
        # should be logged in now
        self.assertTrue(User.objects.filter(username="user2").exists())


class ProfileTests(TestCase):
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

    def test_profile_page(self):  # pragma: no cover
        response = self.client.get("/profile/")
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        response = self.client.get(reverse("user:profile"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_UserUpdateForm_valid(self):  # pragma: no cover

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
