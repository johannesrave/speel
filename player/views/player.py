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

        song_id = request.GET.get('song_id')

        try:
            playlist = Playlist.objects.get(id=playlist_id)
            songs = playlist.songs.all()
        except Playlist.DoesNotExist:
            print('Requested nonexistent playlist with id ' + str(playlist_id))
            return redirect('player')

        if song_id:
            try:
                song_to_play = songs.get(id=song_id)
            except Song.DoesNotExist:
                print(f'Requested nonexistent song with id {str(song_id)}')
                print(f'Switching instead to first song in playlist: {songs.first().title}')
                song_to_play = songs.first().title
        else:
            print(f'No song_id given as query param')
            print(f'Beginning playback at first song in playlist: {songs.first().title}')
            song_to_play = songs.first().title

        context = {
            "playlist": playlist,
            "songs": songs,
            "song_to_play": song_to_play
        }

        return render(request, 'playlist.html', context)

