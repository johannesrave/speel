from django.shortcuts import render, redirect
from django.urls import reverse

from player.forms import PlaylistForm, DeleteForm
from player.models import Playlist
from player.views.views import GuardedView

class CreatePlaylist(GuardedView):

    @staticmethod
    def get(request):
        playlist_form = PlaylistForm()
        create_playlist = reverse('create_playlist')

        context = {
            'action': create_playlist,
            'form': playlist_form,
            'upload_tracks': True,
            'button_label': 'Playlist erstellen'
        }
        return render(request, 'components/form.html', context)

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
        playlist_form = PlaylistForm(instance=playlist)
        update_playlist = reverse('update_playlist', kwargs={'playlist_id': playlist_id})

        context = {
            'action': update_playlist,
            'form': playlist_form,
            'upload_tracks': True,
            'button_label': 'Playlist speichern',
            'image': playlist.thumbnail_file
        }
        return render(request, 'components/form.html', context)

    @staticmethod
    def post(request, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        playlist_form = PlaylistForm(request.POST, request.FILES, instance=playlist)
        if playlist_form.is_valid():
            playlist_form.save()
            return redirect('edit_library')


class DeletePlaylist(GuardedView):

    @staticmethod
    def get(request, playlist_id):
        delete_form = DeleteForm()
        delete_playlist = reverse('delete_playlist', kwargs={'playlist_id': playlist_id})

        context = {
            'action': delete_playlist,
            'form': delete_form,
            'button_label': 'Playlist löschen',
        }
        return render(request, 'components/form.html', context)

    @staticmethod
    def post(request, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        form = PlaylistForm(request.POST)
        # if form.is_valid():
        playlist.delete()
        return redirect('edit_library')
