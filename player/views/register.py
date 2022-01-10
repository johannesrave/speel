#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages

from player.forms import CreateUserForm


class Register(View):

    context = {'action': reverse('register'),
               'form': form,
               'button_label': 'Registrieren'}
    return render(request, 'pages/register.html', context)
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect('view_library')
        context = {'action': reverse('register'),
                   'form': CreateUserForm(),
                   'button_label': 'Registrieren'}
        return render(request, 'register.html', context)

    @staticmethod
    def post(request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account für {username} wurde erzeugt')
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})
