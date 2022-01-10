from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from player.forms import LoginForm


class Login(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect('library')

        context = {'form': LoginForm()}
        return render(request, 'forms/login.html', context)

    @staticmethod
    def post(request):
        intent_to_logout = request.POST.get('logout', False)
        if intent_to_logout:
            logout(request)
            return redirect('login')

        login_form = LoginForm(request.POST)
        if not login_form.is_valid():
            context = {'form': login_form}
            return render(request, 'forms/login.html', context)

        user = User.objects.get(username=request.POST.get('username'))
        login(request, user)
        destination = request.POST.get('redirect_to', 'library')
        return redirect(destination)
