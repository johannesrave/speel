from pprint import pprint

from django.shortcuts import render, redirect
from django.urls import reverse
from tinytag import TinyTag

from player.forms import TemporaryFileForm, TrackForm
from player.models import TemporaryFile, Artist
from player.views.views import GuardedView


class UploadFile(GuardedView):

    def get(self, request):
        context = {
            'action': reverse('upload_track'),
            'form': TemporaryFileForm(),
            'button_label': 'Datei hochladen',
        }
        return render(request, 'generic/form.html', context)

    def post(self, request):
        temp_file_form = TemporaryFileForm(request.POST, request.FILES)

        if not temp_file_form.is_valid():
            print('Invalid file uploaded! Redirecting back to track_upload')
            return redirect('upload_track')

        temp_file_instance = temp_file_form.save()
        params = f"?temp_file_id={temp_file_instance.id}"
        return redirect(reverse('scan_track') + params)


class ScanFile(GuardedView):

    def get(self, request):
        temp_file_id = request.GET['temp_file_id']

        if not temp_file_id:
            print(f'No temp file query string found. Redirecting to file upload.')
            return redirect('track_upload')

        try:
            file_to_scan = TemporaryFile.objects.get(id=temp_file_id)
        except TemporaryFile.DoesNotExist:
            print(f'Temporary file with id {temp_file_id} does not exist. Redirecting to file upload.')
            return redirect('track_upload')

        mp3_file = TinyTag.get(file_to_scan.file.path)
        title = mp3_file.title or 'Unbekannter Titel'

        artist, _ = Artist.objects.get_or_create(name=(mp3_file.artist or 'Unbekannter Artist'))

        context = {
            'action': reverse('scan_track'),
            'form': TrackForm({
                'title': title,
                'artists': [artist],
            }),
            'hidden_fields': [('temp_file_id', temp_file_id)],
            'button_label': 'Song speichern'
        }
        return render(request, 'generic/form.html', context)

    def post(self, request):
        temp_file_id = request.POST.get('temp_file_id')
        track_to_save = TrackForm(request.POST)

        try:
            temp_file = TemporaryFile.objects.get(id=temp_file_id)
        except TemporaryFile.DoesNotExist:
            print(f'Requested nonexistent TemporaryFile with id {temp_file_id}')
            print(f' Redirecting to file upload.')
            return redirect('upload_track')

        if not track_to_save.is_valid():
            pprint('SongForm not valid! Rerendering to correct entries')

            context = {
                'action': reverse('scan_track'),
                'form': track_to_save,
                'temp_file_id': temp_file_id,
                'button_label': 'Song speichern'
            }
            return render(request, 'generic/form.html', context)

        else:
            saved_track = track_to_save.save(commit=False)
            saved_track.audio_file = temp_file.file
            saved_track.duration = TinyTag.get(temp_file.file.path).duration
            saved_track.save()
            temp_file.delete()
            pprint(f'Song {saved_track.title} has been uploaded! Redirecting back to upload_track')
            return redirect('upload_track')