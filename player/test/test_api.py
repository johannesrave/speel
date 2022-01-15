from pprint import pprint

from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from player.models import Audiobook


class AudiobookListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 audiobooks for pagination tests
        number_of_audiobooks = 13

        for audiobook_id in range(number_of_audiobooks):
            Audiobook.objects.create(
                name=f'Christian {audiobook_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/audiobook/')
        pprint(response)
        self.assertEqual(response.status_code, 200)

    def test_view_url_can_be_reached_via_named_route(self):
        response = self.client.get(reverse('audiobook_list'))
        pprint(response)
        self.assertEqual(response.status_code, 200)

    def test_item_can_be_created_from_json_via_post(self):
        data = {"name": "Created from JSON via HTTP"}
        response = self.client.post(reverse('audiobook_list'), data, content_type='application/json')
        pprint(response)
        created_audiobook = Audiobook.objects.get(name=data['name'])
        # pprint(created_audiobook)
        self.assertIsNotNone(created_audiobook)

    def test_item_can_be_created_from_form_via_post(self):
        name = "Created from FORM via HTTP"
        data = urlencode({"name": name})
        response = self.client.post(reverse('audiobook_list'), data, content_type="application/x-www-form-urlencoded")
        pprint(response)
        created_audiobook = Audiobook.objects.get(name=name)
        # pprint(created_audiobook)
        self.assertIsNotNone(created_audiobook)
