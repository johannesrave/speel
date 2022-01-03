from django.shortcuts import render

from player.models import Playlist
from player.views.views import GuardedView


class Library(GuardedView):

    @staticmethod
    def get(request):
        context = {
            'playlists': Playlist.objects.filter(owner=request.user),
        }
        return render(request, 'library.html', context)
