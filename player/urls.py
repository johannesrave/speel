from django.urls import path
from django.views.generic import RedirectView

import player.views.manage.playlist
from player.models import Playlist, Track
from player.views import player, login, register, api, library, manage

urlpatterns = [
    path('login/', login.Login.as_view(), name='login'),
    path('register/', register.Register.as_view(), name='register'),

    # player pages
    path('library/', library.ViewLibrary.as_view(), name='library'),
    path('playlists/', library.EditLibrary.as_view(), name='playlists'),
    path('player/<uuid:playlist_id>/', player.Player.as_view(), name='play_playlist'),

    # content management pages
    path('playlists/new/', manage.playlist.CreatePlaylist.as_view(),
         name='create_playlist'),
    path('playlists/<uuid:playlist_id>/edit/', manage.playlist.UpdatePlaylist.as_view(),
         name='update_playlist'),
    path('playlists/<uuid:playlist_id>/delete/', manage.playlist.DeletePlaylist.as_view(),
         name='delete_playlist'),


    # HTTP-api 'endpoints'
    path('api/playlists/<uuid:model_id>/', api.SingleView.as_view(),
         {'model': Playlist}, name='playlist_single'),
    path('api/playlists/', api.ListView.as_view(),
         {'model': Playlist}, name='playlist_list'),
    path('api/tracks/<uuid:model_id>/', api.SingleView.as_view(),
         {'model': Track}, name='track_single'),
    path('api/tracks/', api.ListView.as_view(),
         {'model': Track}, name='track_list'),

    # redirect and catch-all
    path('', RedirectView.as_view(pattern_name='library', permanent=False)),
]
