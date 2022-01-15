from django.http import HttpResponseNotFound
from django.shortcuts import render

from player.models import Audiobook
from player.views.views import GuardedView


class Player(GuardedView):

    @staticmethod
    def get(request, audiobook_id):
        try:
            tracklist = Audiobook.objects.get(id=audiobook_id)
        except Audiobook.DoesNotExist:
            return HttpResponseNotFound(f'Requested nonexistent audiobook with id {str(audiobook_id)}')

        audiobook = list(Audiobook.objects.filter(id=audiobook_id).values())[0]

        tracks = list(tracklist.tracks.all().values())

        audiobook['tracks'] = tracks
        audiobook['image'] = tracklist.image.url
        context = {'audiobook': audiobook}

        return render(request, 'pages/player.html', context)
