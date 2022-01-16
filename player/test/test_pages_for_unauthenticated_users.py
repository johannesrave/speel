#!/usr/bin/python
# -*- encoding: utf-8 -*-
from pprint import pprint

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.http import urlencode

from player.models import Audiobook


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

    # TODO fix this test
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
        self.assertContains(response.headers["Location"], '/login/')
