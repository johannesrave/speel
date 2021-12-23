from pprint import pprint

from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from player.models import Track, Playlist
from player.views.views import GuardedView


class Player(GuardedView):

    def get(self, request, playlist_id):

        """
        playlist is requested by playlist id, which always exists.
        if a playlist with that id exists, get its track objects
        if the playlist has a 'last track played', get its id
        if the playlist has a 'timetag in last track played', get it

        render template with the playlist with all file paths and ids loaded into the player,
        with the track id of the last track played and with the timestamp

        """

        track_id = request.GET.get('track_id')

        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return HttpResponseNotFound(f'Requested nonexistent playlist with id {str(playlist_id)}')

        tracks = playlist.tracks.all()

        try:
            last_track_played = playlist.last_track_played
            last_timestamp_played = playlist.last_timestamp_played
        except Track.DoesNotExist:
            last_track_played = None

        # this mixes two concerns: setting the track to play and updating the last track played in the playlist.
        # TODO: these two concerns should be taken apart to get simpler logic or the "setting last track played"
        #  should happen on the client only
        if len(tracks):
            try:
                track_to_play = tracks.get(id=track_id)
                playlist.last_track_played = track_to_play
                playlist.save()
                print(f'Beginning playback at track in playlist and setting as "last_track_played": {track_to_play.title}')
            except Track.DoesNotExist:
                print(f'Requested nonexistent track with id {str(track_id)}')
                if playlist.last_track_played:
                    print(f'Beginning playback at last track played in playlist: {tracks.first().title}')
                    track_to_play = playlist.last_track_played
                else:
                    print(f'Beginning playback at first track in playlist: {tracks.first().title}')
                    track_to_play = tracks.first()
        else:
            print(f'Playlist contains no tracks.')
            print(f' Redirecting to playlist selection.')
            return redirect('library')

        track_list = list(tracks.values())
        pprint(track_list)

        context = {
            "playlist": playlist,
            "tracks": tracks,
            "track_list": track_list,
            "track_to_play": track_to_play
        }

        return render(request, 'player.html', context)

