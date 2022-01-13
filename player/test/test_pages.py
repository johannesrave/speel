from pprint import pprint

from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from player.models import Playlist


class PagesTest(TestCase):

    def test_login_exists_at_desired_location(self):
        response = self.client.get('/login/')
        pprint(response)
        self.assertEqual(response.status_code, 200)

    def test_register_exists_at_desired_location(self):
        response = self.client.get('/register/')
        pprint(response)
        self.assertEqual(response.status_code, 200)

    def test_register_is_registration_form(self):
        response = self.client.get('/register/')
        pprint(response)
        self.assertContains(response, html=True,
                            text='<button '
                                 'class="primary-button" type="submit" formaction="/register/">'
                                 'Registrieren'
                                 '</button>')

    def test_users_can_register(self):
        data = {
            "username": "Peter",
            "email": "peter.lustig@gmail.com",
            "password1": "K!nNT9R!QZ0Y",
            "password2": "K!nNT9R!QZ0Y",
        }
        response = self.client.post('/register/', data=data)
        pprint(response)
        pprint(response.headers)
        self.assertContains(response.headers["Location"], 'login')

    def test_library_exists_at_desired_location(self):
        response = self.client.get('/library/')
        pprint(response)
        self.assertEqual(response.status_code, 200)

    def test_playlists_exists_at_desired_location(self):
        response = self.client.get('/playlists/')
        pprint(response)
        self.assertEqual(response.status_code, 200)

    def test_player_exists_at_desired_location(self):
        response = self.client.get('/player/')
        pprint(response)
        self.assertEqual(response.status_code, 200)

    def test_view_url_can_be_reached_via_named_route(self):
        response = self.client.get(reverse('playlist_list'))
        pprint(response)
        self.assertEqual(response.status_code, 200)

    def test_item_can_be_created_from_json_via_post(self):
        data = {"name": "Created from JSON via HTTP"}
        response = self.client.post(reverse('playlist_list'), data, content_type='application/json')
        pprint(response)
        created_playlist = Playlist.objects.get(name=data['name'])
        # pprint(created_playlist)
        self.assertIsNotNone(created_playlist)

    def test_item_can_be_created_from_form_via_post(self):
        name = "Created from FORM via HTTP"
        data = urlencode({"name": name})
        response = self.client.post(reverse('playlist_list'), data, content_type="application/x-www-form-urlencoded")
        pprint(response)
        created_playlist = Playlist.objects.get(name=name)
        # pprint(created_playlist)
        self.assertIsNotNone(created_playlist)
