from datetime import datetime
from pprint import pprint

import requests
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse

class PlaylistListViewTest(LiveServerTestCase):
    credentials = None

    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('secret')
        user.save()

        self.logged_in = self.client.login(username='testuser', password='secret')

    def test_login(self):
        self.assertTrue(self.logged_in)

    def test_view_url_exists_at_desired_location(self):

        # response = self.client.get(reverse('player'))
        response = requests.get(self.live_server_url + reverse('player'))
        pprint(response.__dict__)
        self.assertEqual(response.status_code, 200)
