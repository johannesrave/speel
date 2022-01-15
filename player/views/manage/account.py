#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.shortcuts import render

from player.forms import UpdateUserForm
from player.views.views import GuardedView


class UpdateAccount(GuardedView):

    @staticmethod
    def get(request):
        user = request.user
        context = {
            'form': UpdateUserForm(instance=user),
        }
        return render(request, 'forms/account.html', context)

    @staticmethod
    def post(request):
        user = request.user
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        context = {
            'form': form,
        }
        return render(request, 'forms/account.html', context)
