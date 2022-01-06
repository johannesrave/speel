import io
import os
import random

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datastructures import MultiValueDict

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
        form = PlaylistForm()
        context = {
            'action': reverse('create_playlist'),
            'form': form,
            'button_label': 'Playlist erstellen'
        }
        return render(request, 'generic/form.html', context)

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
        form = PlaylistForm(instance=playlist)
        action = reverse('update_playlist', kwargs={'playlist_id': playlist_id})

        context = {
            'action': action,
            'form': form,
            'button_label': 'Playlist speichern',
            'image': playlist.image
        }
        return render(request, 'generic/form.html', context)

    @staticmethod
    def post(request, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        form = PlaylistForm(request.POST, request.FILES, instance=playlist)
        if form.is_valid():
            playlist = form.save()
            return redirect('update_playlist', playlist_id=playlist.id)


def delete_playlist(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    playlist.delete()

    return redirect('update_or_delete_playlist_overview')
