from django.shortcuts import render

from player.views.views import GuardedView


class ViewLibrary(GuardedView):

    @staticmethod
    def get(request):
        playlists = request.user.owner.playlist_set.all()
        context = {'playlists': playlists}
        return render(request, 'pages/library.html', context)


class EditLibrary(GuardedView):

    @staticmethod
    def get(request):
        playlists = request.user.owner.playlist_set.all()
        context = {'playlists': playlists}
        return render(request, 'pages/playlists.html', context)
