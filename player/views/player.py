from django.http import HttpResponseNotFound
from django.shortcuts import render

from player.models import Audiobook
from player.views.views import GuardedView


class Player(GuardedView):

    @staticmethod
    def get(request, playlist_id):
        try:
            tracklist = Audiobook.objects.get(id=playlist_id)
        except Audiobook.DoesNotExist:
            return HttpResponseNotFound(f'Requested nonexistent playlist with id {str(playlist_id)}')

        playlist = list(Audiobook.objects.filter(id=playlist_id).values())[0]

        tracks = list(tracklist.tracks.all().values())

        playlist['tracks'] = tracks
        playlist['image'] = tracklist.image.url
        context = {'playlist': playlist}

        return render(request, 'pages/player.html', context)
