from django.urls import path, re_path
from django.views.generic import RedirectView

import player.views.manage.index
import player.views.manage.playlist
import player.views.manage.upload_file
from player.models import Playlist, Track
from player.views import player, login, api, library, manage

urlpatterns = [
    path('login/', login.Login.as_view(), name='login'),

    # player pages
    path('library/', library.ViewLibrary.as_view(), name='view_library'),
    path('library/edit/', library.EditLibrary.as_view(), name='edit_library'),
    path('player/<uuid:playlist_id>/', player.Player.as_view(), name='play_playlist'),

    # content management pages
    path('playlists/create/', manage.playlist.CreatePlaylist.as_view(),
         name='create_playlist'),
    path('playlists/update/<uuid:playlist_id>/', manage.playlist.UpdatePlaylist.as_view(),
         name='update_playlist'),
    path('playlists/delete/<uuid:playlist_id>/', manage.playlist.DeletePlaylist.as_view(),
         name='delete_playlist'),
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
    path('', RedirectView.as_view(pattern_name='view_library', permanent=False)),
    # should be a 404 and then redirect
    # re_path(r'^player/.*$', RedirectView.as_view(pattern_name='library', permanent=False))
]
