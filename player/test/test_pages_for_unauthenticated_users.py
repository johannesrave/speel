#!/usr/bin/python
# -*- encoding: utf-8 -*-
from pprint import pprint

from django.contrib.auth.models import User
from django.test import TestCase

class PagesTestUnauthenticatedUser(TestCase):

    def setUp(self):
        self.client.logout()

    def test_login_exists_at_desired_location(self):
        response = self.client.get('/account/login/')
        pprint(response)
        self.assertEqual(response.status_code, 200)

    def test_register_exists_at_desired_location(self):
        response = self.client.get('/account/register/')
        pprint(response)
        self.assertEqual(response.status_code, 200)

    def test_register_is_registration_form(self):
        response = self.client.get('/account/register/')
        pprint(response)
        self.assertContains(response, html=True,
                            text='<button '
                                 'class="primary-button" type="submit" formaction="/account/register/">'
                                 'Registrieren'
                                 '</button>')

    def test_register(self):
        data = {
            "username": "Peter",
            "email": "peter.lustig@gmail.com",
            "password1": "K!nNT9R!QZ0Y",
            "password2": "K!nNT9R!QZ0Y",
        }
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='Peter')
        self.client.post('/account/register/', data=data)
        assert_user_exists('Peter')

    def test_username_cant_be_registered_twice(self):
        data = {
            "username": "Peter",
            "email": "peter.lustig@gmail.com",
            "password1": "K!nNT9R!QZ0Y",
            "password2": "K!nNT9R!QZ0Y",
        }
        data2 = {
            "username": "Peter",
            "email": "anderer.peter@gmail.com",
            "password1": "K!nNT9R!QZ0Y",
            "password2": "K!nNT9R!QZ0Y",
        }
        self.client.post('/account/register/', data=data)
        self.assertEqual(User.objects.get(username='Peter').email, "peter.lustig@gmail.com")
        self.client.post('/account/register/', data=data2)
        self.assertEqual(User.objects.get(username='Peter').email, "peter.lustig@gmail.com")

    def test_successful_register_redirects_to_login(self):
        data = {
            "username": "Peter",
            "email": "peter.lustig@gmail.com",
            "password1": "K!nNT9R!QZ0Y",
            "password2": "K!nNT9R!QZ0Y",
        }
        response = self.client.post('/account/register/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/')

    def test_unauthenticated_user_is_redirected_to_login_if_trying_to_access_account_page(self):
        response = self.client.get('/account/')
        pprint(response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?redirect_to=/account/')

    def test_unauthenticated_user_can_access_passwort_reset_page(self):
        response = self.client.get('/account/password/reset/')
        pprint(response)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_is_redirected_to_login_if_trying_to_access_audiobooks_page(self):
        response = self.client.get('/audiobooks/')
        pprint(response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?redirect_to=/audiobooks/')

    def test_unauthenticated_user_is_redirected_to_login_if_trying_to_access_create_audiobooks_page(self):
        response = self.client.get('/audiobooks/new/')
        pprint(response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?redirect_to=/audiobooks/new/')

def assert_user_exists(username):
    User.objects.get(username=username)

