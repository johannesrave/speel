from pprint import pprint

from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from player.models import Audiobook


class AudiobookListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 playlists for pagination tests
        number_of_playlists = 13

        for playlist_id in range(number_of_playlists):
            Audiobook.objects.create(
                name=f'Christian {playlist_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/playlist/')
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
        created_playlist = Audiobook.objects.get(name=data['name'])
        # pprint(created_playlist)
        self.assertIsNotNone(created_playlist)

    def test_item_can_be_created_from_form_via_post(self):
        name = "Created from FORM via HTTP"
        data = urlencode({"name": name})
        response = self.client.post(reverse('playlist_list'), data, content_type="application/x-www-form-urlencoded")
        pprint(response)
        created_playlist = Audiobook.objects.get(name=name)
        # pprint(created_playlist)
        self.assertIsNotNone(created_playlist)
