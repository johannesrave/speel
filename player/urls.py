from django.urls import path, re_path
from django.views.generic import RedirectView

import player.views.manage.index
import player.views.manage.playlist
import player.views.manage.track
import player.views.manage.library
import player.views.manage.upload_file
from player.models import Playlist, Track
from player.views import player, login, register, api, library, manage

urlpatterns = [
    path('login/', login.Login.as_view(), name='login'),
    path('register/', register.Register.as_view(), name='register'),

    # player pages
    path('library/', library.Library.as_view(), name='library'),
    path('player/<uuid:playlist_id>/', player.Player.as_view(), name='play_playlist'),

    # content management pages
    path('manage/', manage.index.Index.as_view(), name='manage_content'),
    path('manage/playlist/create',
         manage.playlist.CreatePlaylist.as_view(),
         name='create_playlist'),
    path('manage/playlist/<uuid:playlist_id>/',
         manage.playlist.UpdatePlaylist.as_view(),
         name='update_playlist'),
    path('manage/playlist/delete/<uuid:playlist_id>/',
         manage.playlist.delete_playlist,
         name='delete_playlist'),
    path('manage/playlist/all',
         manage.library.Library.as_view(),
         name='update_or_delete_playlist_overview'),
    path('manage/track/<uuid:track_id>/',
         manage.track.UpdateTrack.as_view(),
         name='update_track'),
    path('manage/track/delete/<uuid:track_id>/',
         manage.track.delete_track,
         name='delete_track'),
    path('manage/track/all',
         manage.track.TrackOverview.as_view(),
         name='update_or_delete_track_overview'),
    # path('playlist/create', manage.playlist.Playlist.as_view(), name='create_playlist'),
    path('upload/', manage.upload_file.UploadFile.as_view(), name='upload_track'),
    path('scan/', manage.upload_file.ScanFile.as_view(), name='scan_track'),

    # api 'endpoints'
    path('api/playlists/<uuid:model_id>/', api.SingleView.as_view(),
         {'model': Playlist}, name='playlist_single'),
    path('api/playlists/', api.ListView.as_view(),
         {'model': Playlist}, name='playlist_list'),
    path('api/tracks/<uuid:model_id>/', api.SingleView.as_view(),
         {'model': Track}, name='track_single'),
    path('api/tracks/', api.ListView.as_view(),
         {'model': Track}, name='track_list'),

    # redirect and catch-all
    path('', RedirectView.as_view(pattern_name='library', permanent=True)),
    # should be a 404 and then redirect
    re_path(r'^player/.*$', RedirectView.as_view(pattern_name='library', permanent=False))
]
