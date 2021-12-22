from pprint import pprint

from django.shortcuts import render, redirect
from player.models import Song, Playlist
from player.views.views import GuardedView


class Player(GuardedView):

    def get(self, request, playlist_id):

        song_id = request.GET.get('song_id')

        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            print(f'Requested nonexistent song with id {str(playlist_id)}')
            print(f' Redirecting to playlist selection.')
            return redirect('library')

        songs = playlist.songs.all()

        # this mixes two concerns: setting the song to play and updating the last song played in the playlist.
        # TODO: these two concerns should be taken apart to get simpler logic.
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

        song_list = list(songs.values())
        pprint(song_list)

        context = {
            "playlist": playlist,
            "songs": songs,
            "song_list": song_list,
            "song_to_play": song_to_play
        }

        return render(request, 'player.html', context)

