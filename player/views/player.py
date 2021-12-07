from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from player.models import Song, Playlist


class GuardedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


class Index(GuardedView):

    def get(self, request):
        context = {
            'playlists': Playlist.objects.all(),
        }
        return render(request, 'index.html', context)


class PlaylistView(GuardedView):

    def get(self, request, playlist_id):

        try:
            playlist = Playlist.objects.get(id=playlist_id)
            context = {
                "playlist": playlist,
                "songs": playlist.songs.all()
            }
            pprint(context)
            return render(request, 'playlist.html', context)
        except Playlist.DoesNotExist:
            print('Requested nonexistent playlist with id ' + str(playlist_id))
            return redirect('player')


class SongView(GuardedView):

    def post(self, request):
        pass