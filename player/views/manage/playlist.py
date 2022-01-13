import random
from pprint import pprint

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tinytag import TinyTag

from player.forms import UpdatePlaylistForm, CreatePlaylistForm
from player.models import Track, User
from player.views.views import GuardedView


class CreatePlaylist(GuardedView):

    @staticmethod
    def get(request):
        context = {
            'form': CreatePlaylistForm(),
        }
        return render(request, 'forms/create-playlist.html', context)

    @staticmethod
    def post(request):
        form = CreatePlaylistForm(request.POST, request.FILES)

        if not form.is_valid():
            pprint(form.errors)
            context = {
                'action': reverse('create_playlist'),
                'form': form,
            }
            return render(request, 'forms/create-playlist.html', context)

        playlist = form.save(commit=False)

        save_user(request, playlist)
        save_posted_image_or_default(request, playlist)
        save_all_posted_tracks(request, playlist)

        playlist.save()
        print(playlist.image.name)

        return redirect('update_playlist', playlist_id=playlist.id)


def save_user(request, playlist):
    user: User = request.user
    playlist.user = user


def save_posted_image_or_default(request, playlist):
    image = request.FILES.get('image', None)
    print(f'image in request: {image}')
    if not image:
        playlist.image.name = pick_random_default_image_path()
    else:
        playlist.image = image


def save_all_posted_tracks(request, playlist):
    playlist.save()
    tracks = get_tracks(request)
    playlist.tracks.set(tracks)


def pick_random_default_image_path():
    random.seed()
    value = random.randint(1, 10)
    image_path = f'/default_images/default_img{value}.jpg'
    return image_path


def get_tracks(request: HttpRequest):
    files = request.FILES.getlist('new_tracks')
    tracks = []

    for file in files:
        data = get_metadata(file)
        track = Track.objects.create(**data)
        track.save()
        pprint(f'Song {track.title} has been scanned and uploaded!')
        tracks.append(track)  # TODO: save all tracks in bulk
    return tracks


def get_metadata(audio_file):
    pprint(audio_file)
    file_name = str(audio_file.name)
    tag = TinyTag.get(audio_file.temporary_file_path())

    return {
        'title': tag.title or file_name,
        'duration': tag.duration,
        'audio_file': audio_file,
    }


class UpdatePlaylist(GuardedView):

    @staticmethod
    def get(request, playlist_id):
        playlist = retrieve_playlist_if_owned(request.user, playlist_id)
        if not playlist:
            return redirect('playlists')
        playlist_form = UpdatePlaylistForm(instance=playlist)

        context = {
            'form': playlist_form,
            'playlist_id': playlist_id,
            'image': playlist.image,
        }
        return render(request, 'forms/update-playlist.html', context)

    @staticmethod
    def post(request, playlist_id):
        playlist = retrieve_playlist_if_owned(request.user, playlist_id)
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


def retrieve_playlist_if_owned(user, playlist_id):
    return user.playlist_set.all().get(id=playlist_id)


class DeletePlaylist(GuardedView):

    @staticmethod
    def get(request, playlist_id):
        playlist = retrieve_playlist_if_owned(request.user, playlist_id)
        if not playlist:
            return redirect('playlists')
        context = {
            'playlist_id': playlist_id
        }
        return render(request, 'forms/delete-playlist.html', context)

    @staticmethod
    def post(request, playlist_id):
        playlist = retrieve_playlist_if_owned(request.user, playlist_id)
        if playlist:
            playlist.delete()
        return redirect('playlists')
