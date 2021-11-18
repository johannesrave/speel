from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if not user:
            return HttpResponse.status_code(403)

        login(request, user)
        return redirect(request.POST.get('redirect_to', 'player'))


class Logout(View):
    def get(self, request):
        return redirect('login')

    def post(self, request):
        intent_to_logout = request.POST.get('logout', False)
        if intent_to_logout:
            logout(request)
            return redirect('login')
