import random
from pprint import pprint

from django.shortcuts import render, redirect
from django.urls import reverse
from tinytag import TinyTag

from audioplayer.settings import MEDIA_ROOT
from player.forms import UpdateAudiobookForm, CreateAudiobookForm
from player.models import Track, User
from player.views.views import GuardedView


class CreateAudiobook(GuardedView):

    @staticmethod
    def get(request):
        context = {
            'form': CreateAudiobookForm(),
        }
        return render(request, 'forms/create-playlist.html', context)

    @staticmethod
    def post(request):
        # request.upload_handlers = [TemporaryFileUploadHandler(request)]
        form = CreateAudiobookForm(request.POST, request.FILES)

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
    files = request.FILES.getlist('new_tracks')

    _tracks = Track.objects.bulk_create(
        [Track(audio_file=file, playlist=playlist) for file in files])

    for track in _tracks:
        tag = TinyTag.get(f'{MEDIA_ROOT}/{track.audio_file.name}')

        track.title = tag.title or track.audio_file.name
        track.duration = tag.duration

        pprint(f'Song {track.title} has been scanned and uploaded!')

    Track.objects.bulk_update(_tracks, ['title', 'duration'])


def pick_random_default_image_path():
    random.seed()
    value = random.randint(1, 10)
    image_path = f'/default_images/default_img{value}.jpg'
    return image_path


class UpdateAudiobook(GuardedView):

    @staticmethod
    def get(request, playlist_id):
        playlist = retrieve_playlist_if_owned(request.user, playlist_id)
        if not playlist:
            return redirect('playlists')
        playlist_form = UpdateAudiobookForm(instance=playlist)

        context = {
            'form': playlist_form,
            'playlist_id': playlist_id,
            'playlist': playlist,
        }
        return render(request, 'forms/update-playlist.html', context)

    @staticmethod
    def post(request, playlist_id):
        playlist = retrieve_playlist_if_owned(request.user, playlist_id)
        form = UpdateAudiobookForm(request.POST, request.FILES, instance=playlist)
        if not form.is_valid():
            pprint(form.errors)
            context = {
                'form': form,
                'playlist_id': playlist_id,
            }
            return render(request, 'forms/create-playlist.html', context)

        form.save()
        return redirect('playlists')


class DeleteAudiobook(GuardedView):

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


def retrieve_playlist_if_owned(user, playlist_id):
    return user.playlist_set.all().get(id=playlist_id)
