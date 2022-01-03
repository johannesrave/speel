#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse


def register_page(request):
    form = UserCreationForm

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'action': reverse('register'),
               'form': form,
               'button_label': 'Registrieren'}
    return render(request, 'register.html', context)
