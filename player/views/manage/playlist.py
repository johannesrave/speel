import io
import os
import random

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datastructures import MultiValueDict

from player.forms import PlaylistForm, DeleteForm
from player.models import Playlist
from audioplayer.settings import MEDIA_ROOT
from player.forms import PlaylistForm
from player.models import Playlist
from player.views.views import GuardedView


def get_random_default_image():
    random.seed()
    value = random.randint(1, 10)
    return f'{MEDIA_ROOT}/default_images/default_img{value}.jpg'


def is_no_image_attached(request):
    return len(request.FILES) == 0


def create_random_image():
    image_path = get_random_default_image()
    img = Image.open(image_path)
    img.save(io.BytesIO(), format='JPEG')
    return InMemoryUploadedFile(open(image_path, 'rb'),
                                'image',
                                image_path,
                                'image/jpg',
                                os.path.getsize(image_path),
                                None,
                                {})


def cleanup_post(post):
    del post.copy()['image']
    return post

class CreatePlaylist(GuardedView):

    @staticmethod
    def get(request):
        context = {
            'action': reverse('create_playlist'),
            'form': PlaylistForm(),
            'button_label': 'Playlist erstellen'
        }
        return render(request, 'upload_track.html', context)

    @staticmethod
    def post(request):
        files = request.FILES
        if is_no_image_attached(request):
            files = MultiValueDict({'image': [create_random_image()]})
            request.POST = cleanup_post(request.POST)
        form = PlaylistForm(data=request.POST, files=files)
        if form.is_valid():
            playlist = form.save()
            return redirect('play_playlist', playlist_id=playlist.id)


class UpdatePlaylist(GuardedView):

    @staticmethod
    def get(request, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        update_playlist = reverse('update_playlist', kwargs={'playlist_id': playlist_id})

        context = {
            'action': update_playlist,
            'form': PlaylistForm(instance=playlist),
            'button_label': 'Playlist speichern',
            'image': playlist.image
        }
        return render(request, 'upload_track.html', context)

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
