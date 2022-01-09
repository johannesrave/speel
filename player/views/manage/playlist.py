from pprint import pprint
from typing import Union, List, Any, Optional

from django.core.files.uploadedfile import TemporaryUploadedFile, SimpleUploadedFile, UploadedFile
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tinytag import TinyTag

from player.forms import UpdatePlaylistForm, CreatePlaylistForm, CreateTrackForm
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

        # pprint(request.FILES)
        # pprint(dict(request.FILES))
        pprint(request.FILES.getlist('new_tracks'))
        files: Union[Optional[list[TemporaryUploadedFile]], Any] = request.FILES.getlist('new_tracks')
        tracks = []

        for file in files:
            print()
            print(f'Working on file {file} at {file.temporary_file_path()}')

            data = CreatePlaylist.get_metadata(file)

            print(data)

            track = Track.objects.create(**data)
            track.save()

            # TODO: get files from temp storage into tracks-field of playlist
            # track = track_form.save(commit=False)
            # CreatePlaylist.populate_track_from_tag(track)
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

'''
print(f'temp file object:  {file}')
print(f'file object:  {file.file}')
# print(f'file object:  {file.}')
# pprint(f'{file.file}')

data = {
    'test': 'This validates.',
    'test_file': UploadedFile(file),
    'audio_file': file,
}
track_form = CreateTrackForm(data)

# print(track_form)
# pprint(f'form: {track_form}')
print(f'bound form to:  {track_form.data}')

# pprint(track_form.is_bound)
# track_form.audio_file = file.temporary_file_path()
if not track_form.is_valid():
    # pprint(track_form.fields['audio_file'])
    # pprint(track_form.cleaned_data)
    print(track_form.errors)
    continue
'''


    # @staticmethod
    # def populate_track_from_tag(track):
    #     audio_file = track.audio_file.file
    #     pprint(audio_file)
    #     file_name = str(audio_file.temporary_file_path().split('.')[-2])
    #     tag = TinyTag.get(audio_file.temporary_file_path())
    #     track.duration = tag.duration
    #     track.title = tag.title or file_name or 'Unbekannter Track'


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
        # form = PlaylistForm(request.POST)
        # if form.is_valid():
        playlist.delete()
        return redirect('playlists')
