#!/usr/bin/python
# -*- encoding: utf-8 -*-
from pprint import pprint

from django.contrib.auth.models import User
from django.test import TestCase


@staticmethod
def assert_user_exists(username):
    User.objects.get(username=username)


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

    def test_register(self):
        data = {
            "username": "Peter",
            "email": "peter.lustig@gmail.com",
            "password1": "K!nNT9R!QZ0Y",
            "password2": "K!nNT9R!QZ0Y",
        }
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='Peter')
        self.client.post('/register/', data=data)
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
        self.client.post('/register/', data=data)
        self.assertEqual(User.objects.get(username='Peter').email, "peter.lustig@gmail.com")
        self.client.post('/register/', data=data2)
        self.assertEqual(User.objects.get(username='Peter').email, "peter.lustig@gmail.com")

    def test_successful_register_redirects_to_login(self):
        data = {
            "username": "Peter",
            "email": "peter.lustig@gmail.com",
            "password1": "K!nNT9R!QZ0Y",
            "password2": "K!nNT9R!QZ0Y",
        }
        response = self.client.post('/register/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')
