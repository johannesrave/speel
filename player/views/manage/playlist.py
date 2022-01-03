from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from player.forms import PlaylistForm
from player.models import Playlist, Track
from player.views.views import GuardedView


def save_form_if_valid(form):
    if form.is_valid():
        playlist = form.save()
        return redirect('play_playlist', playlist_id=playlist.id)


class CreatePlaylist(GuardedView):

    @staticmethod
    def get(request):
        form = PlaylistForm()
        context = {
            'action': reverse('create_playlist'),
            'form': form,
            'button_label': 'Playlist erstellen'
        }
        return render(request, 'generic/form.html', context)

    @staticmethod
    def post(request):
        form = PlaylistForm(request.POST, request.FILES)
        return save_form_if_valid(form)


class UpdatePlaylist(GuardedView):

    @staticmethod
    def get(request: HttpRequest, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        form = PlaylistForm(instance=playlist)
        action = reverse('update_playlist', kwargs={'playlist_id': playlist_id})

        context = {
            'action': action,
            'form': form,
            'button_label': 'Playlist speichern',
        }
        return render(request, 'generic/form.html', context)

    @staticmethod
    def post(request, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        form = PlaylistForm(request.POST, request.FILES, instance=playlist)
        return save_form_if_valid(form)

#class DeletePlaylist(GuardedView):

