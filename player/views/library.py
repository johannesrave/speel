from django.shortcuts import render

from player.models import Audiobook
from player.views.views import GuardedView


class ViewLibrary(GuardedView):

    @staticmethod
    def get(request):
        playlists = Audiobook.objects.filter(user=request.user)
        context = {'playlists': playlists}
        return render(request, 'pages/library.html', context)


class EditLibrary(GuardedView):

    @staticmethod
    def get(request):
        playlists = Audiobook.objects.filter(user=request.user)
        context = {'playlists': playlists}
        return render(request, 'pages/playlists.html', context)
