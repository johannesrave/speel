from django.http import HttpResponseNotFound
from django.shortcuts import render

from player.models import Playlist
from player.views.views import GuardedView


class Player(GuardedView):

    def get(self, request, playlist_id):
        try:
            tracklist = Playlist.objects.get(id=playlist_id)
            thumbnail_url = tracklist.thumbnail_file.thumbnails.large.url
        except Playlist.DoesNotExist:
            return HttpResponseNotFound(f'Requested nonexistent playlist with id {str(playlist_id)}')

        tracks = list(tracklist.tracks.all().values())

        playlist = list(Playlist.objects.filter(id=playlist_id).values())[0]
        playlist['tracks'] = tracks

        context = {
            'playlist': playlist,
            'thumbnail_url': thumbnail_url,
        }

        return render(request, 'player.html', context)
