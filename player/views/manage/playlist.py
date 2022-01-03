from django.shortcuts import render, redirect
from django.urls import reverse

from player.forms import PlaylistForm
from player.views.views import GuardedView


class Playlist(GuardedView):

    def get(self, request):
        context = {
            'action': reverse('create_playlist'),
            'form': PlaylistForm(),
            'button_label': 'Playlist erstellen',
        }
        return render(request, 'generic/form.html', context)

    def post(self, request):
        playlist_form = PlaylistForm(request.POST, request.FILES)

        if not playlist_form.is_valid():
            context = {
                'action': reverse('create_playlist'),
                'form': playlist_form,
                'button_label': 'Playlist erstellen',
            }
            return render(request, 'generic/form.html', context)

        playlist = playlist_form.save()
        return redirect('play_playlist', playlist_id=playlist.id)


class CreatePlaylist(GuardedView):
    pass


class UpdatePlaylist(GuardedView):
    pass


class DeletePlaylist(GuardedView):
    pass
