from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        intent_to_logout = request.POST.get('logout', False)
        if intent_to_logout:
            logout(request)
            return redirect('login')

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if not user or not user.is_active:
            print('username or password not correct')
            return redirect('login')

        login(request, user)
        return redirect(request.POST.get('redirect_to', 'library'))
