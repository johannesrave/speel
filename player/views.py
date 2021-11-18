from pprint import pprint

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from player.models import Song, Playlist


class Index(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        song_id = request.GET.get('song_id', False)
        playlist_id = request.GET.get('playlist_id', False)

        context = {
            'playlists': [p for p in Playlist.objects.all()],
        }
        if playlist_id:
            try:
                playlist = Playlist.objects.get(id=playlist_id)
                context["playlist"] = playlist
                context["playlists"].insert(0, playlist)
                context["songs"] = playlist.songs.all()
            except Playlist.DoesNotExist:
                return redirect('player')

            if song_id:
                try:
                    context["song_to_play"] = Song.objects.get(id=song_id)
                except Song.DoesNotExist:
                    return redirect('player')

        pprint(context)
        return render(request, 'index.html', context)


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
