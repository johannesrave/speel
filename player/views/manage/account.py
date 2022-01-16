#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from player.forms import UpdateUserForm, CreateUserForm, LoginForm
from player.views.views import GuardedView


class UpdateAccount(GuardedView):

    @staticmethod
    def get(request):
        user = request.user
        context = {
            'form': UpdateUserForm(instance=user),
        }
        return render(request, 'forms/account-update.html', context)

    @staticmethod
    def post(request):
        user = request.user
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        context = {
            'form': form,
        }
        return render(request, 'forms/account-update.html', context)


class Register(View):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect('library')
        context = {
            'form': CreateUserForm()
        }
        return render(request, 'forms/account-create.html', context)

    @staticmethod
    def post(request):
        form = CreateUserForm(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, 'forms/account-create.html', context)

        user: User = form.save()
        messages.success(request, f'Account für {user.username} wurde erstellt.')
        return redirect('login')


class Login(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect('library')

        context = {'form': LoginForm()}
        return render(request, 'forms/account-login.html', context)

    @staticmethod
    def post(request):
        intent_to_logout = request.POST.get('logout', False)
        if intent_to_logout:
            logout(request)
            return redirect('login')

        login_form = LoginForm(request.POST)
        if not login_form.is_valid():
            context = {'form': login_form}
            return render(request, 'forms/account-login.html', context)

        user = User.objects.get(username=request.POST.get('username'))
        # TODO: check if request.user already exists
        login(request, user)
        destination = request.POST.get('redirect_to', 'library')
        return redirect(destination)