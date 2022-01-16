from pprint import pprint

from django.contrib.auth.models import User
from django.test import TestCase, Client

from player.models import Audiobook


class PagesTest(TestCase):

    def setUp(self):
        self.create_and_login_user()

    def create_and_login_user(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()

        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_logged_in_user_is_redirected_to_library_if_trying_to_access_login_page(self):
        response = self.client.get('/login/')
        pprint(response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/library/')

    def test_logged_in_user_is_redirected_to_library_if_trying_to_access_register_page(self):
        response = self.client.get('/register/')
        pprint(response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/library/')

    def test_library_exists_at_desired_location(self):
        response = self.client.get('/library/')
        pprint(response)
        self.assertEqual(response.status_code, 200)

    def test_audiobooks_exists_at_desired_location(self):
        response = self.client.get('/audiobooks/')
        pprint(response)
        self.assertEqual(response.status_code, 200)

    # TODO create Audiobook for user, check if he can access it with /player/id
    # TODO check if another user cant access this audiobook
    # def test_player_exists_at_desired_location(self):
    #     audiobook = Audiobook.objects.create(name=)
    #     response = self.client.get('/player/')
    #     pprint(response)
    #     self.assertEqual(response.status_code, 200)
