#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from player.forms import CreateUserForm


class Register(View):

    @staticmethod
    def get(request):
        context = {'action': reverse('register'),
                   'form': CreateUserForm,
                   'button_label': 'Registrieren'}
        return render(request, 'register.html', context)

    @staticmethod
    def post(request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
