from pprint import pprint

from django.http import HttpRequest
import io
import os
import random

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect
from django.urls import reverse
from tinytag import TinyTag
from django.utils.datastructures import MultiValueDict

from player.forms import UpdatePlaylistForm, CreatePlaylistForm
from player.models import Playlist, Track
from audioplayer.settings import MEDIA_ROOT
from player.forms import DeleteForm
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
            'form': CreatePlaylistForm(),
        }
        return render(request, 'forms/create-playlist.html', context)

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
        form = CreatePlaylistForm(request.POST, request.FILES)
        if not form.is_valid():
            pprint(form.errors)
            context = {
                'action': reverse('create_playlist'),
                'form': form,
            }
            return render(request, 'forms/create-playlist.html', context)

        tracks = CreatePlaylist.save_tracks(request)
        playlist = form.save()
        playlist.tracks.set(tracks)
        playlist.save()

        return redirect('update_playlist', playlist_id=playlist.id)

    @staticmethod
    def save_tracks(request: HttpRequest):
        files = request.FILES.getlist('new_tracks')
        tracks = []

        for file in files:
            data = CreatePlaylist.get_metadata(file)
            track = Track.objects.create(**data)
            track.save()
            pprint(f'Song {track.title} has been scanned and uploaded!')
            tracks.append(track)  # TODO: save all tracks in bulk
        return tracks

    @staticmethod
    def get_metadata(audio_file):
        pprint(audio_file)
        file_name = str(audio_file.temporary_file_path().split('.')[-2])
        tag = TinyTag.get(audio_file.temporary_file_path())

        return {
            'title': tag.title or file_name or 'Unbekannter Track',
            'duration': tag.duration,
            'audio_file': audio_file,
        }


class UpdatePlaylist(GuardedView):

    @staticmethod
    def get(request, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        playlist_form = UpdatePlaylistForm(instance=playlist)

        context = {
            'form': playlist_form,
            'playlist_id': playlist_id,
            'image': playlist.image,
        }
        return render(request, 'forms/update-playlist.html', context)

    @staticmethod
    def post(request, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        form = UpdatePlaylistForm(request.POST, request.FILES, instance=playlist)
        if not form.is_valid():
            pprint(form.errors)
            context = {
                'form': form,
                'playlist_id': playlist_id,
            }
            return render(request, 'forms/create-playlist.html', context)

        form.save()
        return redirect('playlists')


class DeletePlaylist(GuardedView):

    @staticmethod
    def get(request, playlist_id):
        context = {
            'playlist_id': playlist_id
        }
        return render(request, 'forms/delete-playlist.html', context)

    @staticmethod
    def post(request, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.delete()
        return redirect('playlists')
