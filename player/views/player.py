from django.http import HttpResponseNotFound
from django.shortcuts import render

from player.models import Playlist
from player.views.views import GuardedView


class Player(GuardedView):

    @staticmethod
    def get(request, playlist_id):
        try:
            tracklist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return HttpResponseNotFound(f'Requested nonexistent playlist with id {str(playlist_id)}')

        tracks = list(tracklist.tracks.all().values())

        playlist = list(Playlist.objects.filter(id=playlist_id).values())[0]
        playlist['tracks'] = tracks
        playlist['thumbnail_file'] = tracklist.thumbnail_file.url
        if tracklist not in Playlist.objects.filter(owner=request.user):
            playlist = []
        context = {
            'playlist': playlist,
        }

        return render(request, 'player.html', context)
