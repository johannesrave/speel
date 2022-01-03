from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from player.forms import LoginForm


class Login(View):
    @staticmethod
    def get(request):
        context = {
            'action': reverse('login'),
            'form': LoginForm(),
            'button_label': 'Anmelden',
        }
        return render(request, 'login.html', context)

    @staticmethod
    def post(request):
        intent_to_logout = request.POST.get('logout', False)
        if intent_to_logout:
            logout(request)
            return redirect('login')

        login_form = LoginForm(request.POST)

        if not login_form.is_valid():
            context = {
                'action': reverse('login'),
                'form': login_form,
                'button_label': 'Anmelden',
            }
            return render(request, 'login.html', context)

        user = User.objects.get(username=request.POST.get('username'))
        login(request, user)

        destination = request.POST.get('redirect_to', 'library')
        return redirect(destination)
