from django.shortcuts import render

from player.models import Playlist
from player.views.views import GuardedView


class ViewLibrary(GuardedView):

    def get(self, request):
        context = {
            'playlists': Playlist.objects.all(),
            'item_template': 'library-view-item.html',
            'edit_library': True
        }
        return render(request, 'library.html', context)


class EditLibrary(GuardedView):

    def get(self, request):
        context = {
            'playlists': Playlist.objects.all(),
            'item_template': 'library-edit-item.html'
        }
        return render(request, 'library.html', context)
