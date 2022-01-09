from pprint import pprint

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tinytag import TinyTag

from player.forms import UpdatePlaylistForm, CreatePlaylistForm
from player.models import Playlist, Track
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
