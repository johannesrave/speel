from django.shortcuts import render

from player.models import Playlist
from player.views.views import GuardedView


class Library(GuardedView):

    def get(self, request):
        context = {
            'playlists': Playlist.objects.all(),
            'show_edit_buttons': True
        }
        return render(request, 'manage/library.html', context)
