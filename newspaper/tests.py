from django.test import TestCase
from django.urls import reverse
from .models import Newspaper, Topic, Redactor
from django.contrib.auth import get_user_model


User = get_user_model()


class AuthenticationTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Sample Topic")
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            topic=self.topic
        )

    def test_login(self):
        response = self.client.post(reverse("login"), {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse("newspaper:index"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_access_protected_view_without_login(self):
        response = self.client.get(reverse("newspaper:newspaper-list"))
        self.assertRedirects(response, f"{reverse("login")}?next={reverse('newspaper:newspaper-list')}")

    def test_access_protected_view_with_login(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse("newspaper:newspaper-list"))
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects_to_login(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
        response = self.client.get(reverse("newspaper:newspaper-list"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('newspaper:newspaper-list')}")
