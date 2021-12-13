from pprint import pprint

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from player.models import Song, Playlist, PlaylistForm


class GuardedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


class LibraryView(GuardedView):

    def get(self, request):

        # get list of playlists from api as json
        playlist_list_url = request.build_absolute_uri(location=reverse('playlist_list'))
        response = requests.get(playlist_list_url)
        playlist_list = response.json()

        # use the json to render the template
        context = {
            'playlists': playlist_list,
        }
        return render(request, 'index.html', context)


class PlayerView(GuardedView):

    def get(self, request, playlist_id):

        song_id = request.GET.get('song_id')

        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            print(f'Requested nonexistent song with id {str(playlist_id)}')
            print(f' Redirecting to playlist selection.')
            return redirect('library')

        songs = playlist.songs.all()

        if len(songs):
            try:
                song_to_play = songs.get(id=song_id)
                playlist.last_song_played = song_to_play
                playlist.save()
                print(f'Beginning playback at song in playlist and setting as "last_song_played": {song_to_play.title}')
            except Song.DoesNotExist:
                print(f'Requested nonexistent song with id {str(song_id)}')
                if playlist.last_song_played:
                    print(f'Beginning playback at last song played in playlist: {songs.first().title}')
                    song_to_play = playlist.last_song_played
                else:
                    print(f'Beginning playback at first song in playlist: {songs.first().title}')
                    song_to_play = songs.first()
        else:
            print(f'Playlist contains no songs.')
            print(f' Redirecting to playlist selection.')
            return redirect('library')

        # pprint(serializers.serialize("json", songs))
        song_list = list(songs.values())
        pprint(song_list)

        context = {
            "playlist": playlist,
            "songs": songs,
            # "songs_json": serializers.serialize("json", songs),
            "song_list": song_list,
            "song_to_play": song_to_play
        }

        return render(request, 'player.html', context)

class PlaylistCreateView(GuardedView):

    def get(self, request):
        context = {
            'action': reverse('create_playlist'),
            'form': PlaylistForm(),
            'button_label': 'Playlist erstellen',
        }
        return render(request, 'upload/form.html', context)

    def post(self, request):
        playlist_form = PlaylistForm(request.POST)

        if not playlist_form.is_valid():
            context = {
                'action': reverse('create_playlist'),
                'form': playlist_form,
                'button_label': 'Playlist erstellen',
            }
            return render(request, 'upload/form.html', context)

        playlist = playlist_form.save()
        return redirect('play_playlist', playlist_id=playlist.id)
