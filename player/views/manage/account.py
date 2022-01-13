#!/usr/bin/python
# -*- encoding: utf-8 -*-
from pprint import pprint

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from player.forms import CreateUserForm
from player.views.views import GuardedView


class ManageAccount(GuardedView):

    @staticmethod
    def get(request):
        user = request.user
        context = {
            'form': CreateUserForm(instance=user),
        }
        return render(request, 'forms/account.html', context)

    @staticmethod
    def post(request):
        user = request.user
        form = CreateUserForm(request.POST, instance=user)
        if not form.is_valid():
            pprint(form.errors)
            context = {
                'action': reverse('account'),
                'form': form,
            }
            return render(request, 'forms/account.html', context)

        user: User = form.save()

        return redirect('library')