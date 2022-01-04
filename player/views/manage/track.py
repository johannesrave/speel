from django.shortcuts import render, redirect
from django.urls import reverse

from player.forms import TrackForm
from player.models import Track
from player.views.views import GuardedView


class UpdateTrack(GuardedView):

    @staticmethod
    def get(request, track_id):
        track = Track.objects.get(id=track_id)
        form = TrackForm(instance=track)
        action = reverse('update_track', kwargs={'track_id': track_id})

        context = {
            'action': action,
            'form': form,
            'button_label': 'Track speichern',
        }
        return render(request, 'generic/form.html', context)

    @staticmethod
    def post(request, track_id):
        track = Track.objects.get(id=track_id)
        form = TrackForm(request.POST, request.FILES, instance=track)
        if form.is_valid():
            form.save()
            return redirect('update_or_delete_track_overview')


class TrackOverview(GuardedView):

    @staticmethod
    def get(request):
        context = {
            'tracks': Track.objects.all(),
        }
        return render(request, 'manage/track_library.html', context)


def delete_track(request, track_id):
    track = Track.objects.get(id=track_id)
    track.delete()

    return redirect('update_or_delete_track_overview')
