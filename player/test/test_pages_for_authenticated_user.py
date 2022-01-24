#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from pprint import pprint

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from player.models import Audiobook


class PagesTestLoggedInUser(TestCase):
    """Test for case user is logged in."""

    def setUp(self):
        self.create_and_login_user()

    def create_and_login_user(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()

        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_logged_in_user_is_redirected_to_library_if_trying_to_access_login_page(self):
        response = self.client.get('/account/login/')
        pprint(response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/library/')

    def test_logged_in_user_is_redirected_to_library_if_trying_to_access_register_page(self):
        response = self.client.get('/account/register/')
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

    def test_audiobook_gets_bound_to_user(self):
        self.create_audiobook_returns_post_request("audiobook_testname")
        audiobook = Audiobook.objects.filter(user=self.user)[0]
        print(audiobook)
        users_audiobook = Audiobook.objects.filter(user=self.user)[0]
        self.assertEqual(users_audiobook, audiobook)

    def test_audiobook_cant_be_accessed_just_by_owner(self):
        self.create_audiobook_returns_post_request("audiobook_with_owner_testuser")

        users_library = self.client.get('/library/')
        self.assertContains(users_library, text='audiobook_with_owner_testuser', html=True)

        self.client.logout()

        other_user = self.login_and_return_other_user()

        other_users_library = self.client.get('/library/')
        self.assertNotContains(other_users_library, text='audiobook_with_owner_testuser', html=True)

        other_users_audiobook = Audiobook.objects.filter(user=other_user)
        self.assertFalse(other_users_audiobook)

    def test_edit_audiobook_page_can_only_be_accessed_with_valid_audiobook_id(self):
        audiobook_id = self.create_audiobook_returns_post_request("audiobook").url.split('/')[2]
        audiobook = Audiobook.objects.get(id=audiobook_id)
        self.assertEqual(audiobook_id, str(audiobook.id))
        edit_path = f'/audiobooks/{audiobook.id}/edit/'
        response = self.client.get(edit_path)
        self.assertContains(response, html=True,
                            text=f'<button type="submit" formaction="/audiobooks/{audiobook.id}/edit/">'
                                 'Änderungen speichern'
                                 '</button>')

        trying_to_access_with_invalid_id = self.client.get(f'/audiobooks/{audiobook.id}1234/edit/')
        self.assertEqual(trying_to_access_with_invalid_id.status_code, 404)

    def test_edit_page_cannot_be_accessed_by_other_user(self):
        audiobook_id = self.create_audiobook_returns_post_request("audiobook").url.split('/')[2]
        audiobook = Audiobook.objects.get(id=audiobook_id)
        self.client.logout()
        other_user = self.login_and_return_other_user()
        edit_path = f'/audiobooks/{audiobook.id}/edit/'
        with self.assertRaises(Audiobook.DoesNotExist):
            self.client.get(edit_path)

    def test_edit_page_can_not_be_accessed_by_unauthenticated_user(self):
        audiobook_id = self.create_audiobook_returns_post_request("audiobook").url.split('/')[2]
        audiobook = Audiobook.objects.get(id=audiobook_id)
        self.client.logout()
        edit_path = f'/audiobooks/{audiobook.id}/edit/'
        response = self.client.get(edit_path)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/account/login/?redirect_to=/audiobooks/{audiobook_id}/edit/')

    def create_audiobook_returns_post_request(self, name):
        data = {'name': name}
        return self.client.post(reverse('create_audiobook'), data=data)

    def login_and_return_other_user(self):
        other_user = User.objects.create(username='other_user')
        other_user.set_password('12345')
        other_user.save()
        self.client.login(username='other_user', password='12345')
        return other_user
