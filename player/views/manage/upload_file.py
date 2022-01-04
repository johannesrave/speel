from pprint import pprint
from urllib.request import Request

from django.shortcuts import render, redirect
from django.urls import reverse
from tinytag import TinyTag

from player.forms import TemporaryFileForm, TrackForm
from player.models import TemporaryFile, Artist
from player.views.views import GuardedView


class UploadFile(GuardedView):

    @staticmethod
    def get(request):
        context = {
            'action': reverse('upload_track'),
            'form': TemporaryFileForm(),
            'button_label': 'Datei hochladen',
        }
        return render(request, 'generic/form.html', context)

    @staticmethod
    def post(request):
        temp_file_form = TemporaryFileForm(request.POST, request.FILES)

        if not temp_file_form.is_valid():
            context = {
                'action': reverse('upload_track'),
                'form': temp_file_form,
                'button_label': 'Datei hochladen',
            }
            return render(request, 'generic/form.html', context)

        temp_file_instance = temp_file_form.save()
        raw_file_name = str(temp_file_form.files.get('file')).split('.')[0].strip()
        params = f"?temp_file_id={temp_file_instance.id}&raw_file_name={raw_file_name}"
        return redirect(reverse('scan_track') + params)


class ScanFile(GuardedView):

    @staticmethod
    def get(request):
        temp_file_id = request.GET['temp_file_id']
        raw_file_name = request.GET['raw_file_name']

        if not temp_file_id:
            print(f'No temp file query string found. Redirecting to file upload.')
            return redirect('track_upload')

        try:
            file_to_scan = TemporaryFile.objects.get(id=temp_file_id)
        except TemporaryFile.DoesNotExist:
            print(f'Temporary file with id {temp_file_id} does not exist. Redirecting to file upload.')
            return redirect('track_upload')

        mp3_file = TinyTag.get(file_to_scan.file.path)
        title = mp3_file.title or raw_file_name or 'Unbekannter Titel'

        artist, _ = Artist.objects.get_or_create(name=(mp3_file.artist or 'Unbekannter Artist'))

        context = {
            'action': reverse('scan_track'),
            'form': TrackForm({
                'title': title,
                'artists': [artist],
            }),
            'hidden_fields': [('temp_file_id', temp_file_id)],
            'button_label': 'Track speichern'
        }
        return render(request, 'generic/form.html', context)

    @staticmethod
    def post(request):
        temp_file_id = request.POST.get('temp_file_id')
        track_to_save = TrackForm(request.POST)

        try:
            temp_file = TemporaryFile.objects.get(id=temp_file_id)
        except TemporaryFile.DoesNotExist:
            print(f'Requested nonexistent TemporaryFile with id {temp_file_id}')
            print(f' Redirecting to file upload.')
            return redirect('upload_track')

        if not track_to_save.is_valid():
            context = {
                'action': reverse('scan_track'),
                'form': track_to_save,
                'temp_file_id': temp_file_id,
                'button_label': 'Track speichern'
            }
            return render(request, 'generic/form.html', context)

        else:
            saved_track = track_to_save.save()
            saved_track.audio_file = temp_file.file
            saved_track.duration = TinyTag.get(temp_file.file.path).duration
            saved_track.save()
            temp_file.delete()
            pprint(f'Song {saved_track.title} has been uploaded! Redirecting back to upload_track')
            return redirect('upload_track')