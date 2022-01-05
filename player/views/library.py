from django.shortcuts import render

from player.models import Playlist
from player.views.views import GuardedView


class ViewLibrary(GuardedView):

    @staticmethod
    def get(request):
        context = {
            'playlists': Playlist.objects.all(),
            'item_template': 'components/library-view-item.html',
            'view_library': True
        }
        return render(request, 'library.html', context)


class EditLibrary(GuardedView):

    @staticmethod
    def get(request):
        context = {
            'playlists': Playlist.objects.all(),
            'item_template': 'components/library-edit-item.html',
            'edit_library': True
        }
        return render(request, 'library.html', context)
