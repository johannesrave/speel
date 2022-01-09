from pprint import pprint

from django.shortcuts import render, redirect
from django.urls import reverse
from tinytag import TinyTag

from player.forms import CreateTrackForm, UpdateTrackForm
from player.models import Track
from player.views.views import GuardedView


class CreateTrack(GuardedView):

    @staticmethod
    def get(request):
        context = {
            'action': reverse('create_track'),
            'form': CreateTrackForm(),
            'button_label': 'Track hochladen',
        }
        return render(request, 'forms/base.html', context)

    @staticmethod
    def post(request):
        track_form = CreateTrackForm(request.FILES)

        if not track_form.is_valid():
            context = {
                'action': reverse('create_track'),
                'form': CreateTrackForm(track_form),
                'button_label': 'Track hochladen',
            }
            return render(request, 'forms/base.html', context)

        track = track_form.save(commit=False)
        CreateTrack.populate_track_from_tag(track)

        track.save()

        pprint(f'Song {track.title} has been scanned and uploaded!')
        pprint(f'Redirecting to update_track')
        return redirect('update_track', track_id=track.id)

    @staticmethod
    def populate_track_from_tag(track):
        audio_file = track.audio_file.file
        pprint(audio_file)
        file_name = str(audio_file.temporary_file_path().split('.')[-2])
        tag = TinyTag.get(audio_file.temporary_file_path())
        track.duration = tag.duration
        track.title = tag.title or file_name or 'Unbekannter Track'


class UpdateTrack(GuardedView):

    @staticmethod
    def get(request, track_id):
        track = Track.objects.get(id=track_id)
        update_track_form = UpdateTrackForm(instance=track)
        update_track_action = reverse('update_track', kwargs={'track_id': track_id})

        context = {
            'action': update_track_action,
            'form': update_track_form,
            'button_label': 'Track speichern',
        }
        return render(request, 'forms/base.html', context)

    @staticmethod
    def post(request, track_id):
        track = Track.objects.get(id=track_id)
        form = UpdateTrackForm(request.POST, instance=track)
        if form.is_valid():
            form.save()
            return redirect('create_track')


class DeleteTrack(GuardedView):

    @staticmethod
    def post(request, track_id):
        track = Track.objects.get(id=track_id)
        track.delete()
        # return redirect('update_or_delete_track_overview')
        return redirect(request.META.get('HTTP_REFERER'))
