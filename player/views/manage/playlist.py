from django.shortcuts import render, redirect
from django.urls import reverse

from player.forms import PlaylistForm, DeleteForm
from player.models import Playlist
from player.views.views import GuardedView

class CreatePlaylist(GuardedView):

    @staticmethod
    def get(request):
        form = PlaylistForm()
        context = {
            'action': reverse('create_playlist'),
            'form': form,
            'button_label': 'Playlist erstellen'
        }
        return render(request, 'generic/../../templates/components/form.html', context)

    @staticmethod
    def post(request):
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save()
            return redirect('play_playlist', playlist_id=playlist.id)


class UpdatePlaylist(GuardedView):

    @staticmethod
    def get(request, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        form = PlaylistForm(instance=playlist)
        action = reverse('update_playlist', kwargs={'playlist_id': playlist_id})

        context = {
            'action': action,
            'form': form,
            'button_label': 'Playlist speichern',
            'image': playlist.thumbnail_file
        }
        return render(request, 'generic/../../templates/components/form.html', context)

    @staticmethod
    def post(request, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        form = PlaylistForm(request.POST, request.FILES, instance=playlist)
        if form.is_valid():
            playlist = form.save()
            return redirect('edit_library')


class DeletePlaylist(GuardedView):

    @staticmethod
    def get(request, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        form = DeleteForm()
        action = reverse('delete_playlist', kwargs={'playlist_id': playlist_id})

        context = {
            'action': action,
            'form': form,
            'button_label': 'Playlist löschen!',
        }
        return render(request, 'generic/../../templates/components/form.html', context)

    @staticmethod
    def post(request, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        form = PlaylistForm(request.POST)
        # if form.is_valid():
        playlist.delete()
        return redirect('edit_library')
