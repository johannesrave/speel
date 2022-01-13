#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.shortcuts import render

from player.forms import OwnerForm
from player.views.views import GuardedView


class UpdateAccount(GuardedView):

    @staticmethod
    def get(request):
        owner = request.user.owner
        context = {
            'form': OwnerForm(instance=owner),
        }
        return render(request, 'forms/account.html', context)

    @staticmethod
    def post(request):
        owner = request.user.owner
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
        context = {
            'form': form,
        }
        return render(request, 'forms/account.html', context)
