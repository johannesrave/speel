from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from player.models import Song, Playlist, PlaylistForm


class GuardedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


class Player(GuardedView):

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
        except Playlist.DoesNotExist:
            print(f'Requested nonexistent song with id {str(playlist_id)}')
            print(f' Redirecting to playlist selection.')
            return redirect('player')

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
            return redirect('player')

        context = {
            "playlist": playlist,
            "songs": songs,
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
        playlist_form = PlaylistForm(request.POST, request.FILES)

        if not playlist_form.is_valid():
            context = {
                'action': reverse('create_playlist'),
                'form': playlist_form,
                'button_label': 'Playlist erstellen',
            }
            return render(request, 'upload/form.html', context)

        playlist = playlist_form.save()
        return redirect('playlist_to_play', playlist_id=playlist.id)
