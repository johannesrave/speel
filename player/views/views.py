#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class GuardedView(LoginRequiredMixin, View):
    """This is a view to ensure just logged in users can enter any view that extends this one."""
    login_url = '/account/login/'
    redirect_field_name = 'redirect_to'
