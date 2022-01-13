#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.shortcuts import render

from player.forms import CreateUserForm
from player.views.views import GuardedView


class UpdateAccount(GuardedView):

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
        if form.is_valid():
            form.save()
        context = {
            'form': form,
        }
        return render(request, 'forms/account.html', context)
