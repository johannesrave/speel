#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from player.forms import CreateUserForm


class Register(View):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect('library')
        context = {
            'action': reverse('register'),
            'form': CreateUserForm()
        }
        return render(request, 'forms/register.html', context)

    @staticmethod
    def post(request):
        form = CreateUserForm(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, 'forms/register.html', context)

        user: User = form.save()
        messages.success(request, f'Account für {user.username} wurde erzeugt')
        return redirect('login')
