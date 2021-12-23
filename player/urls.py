from django.contrib.auth.models import User
from django.urls import path, re_path
from django.views.generic import RedirectView

from player.models import Playlist, Song
from player.views import player, login, api, library, manage

urlpatterns = [
    path('login/', login.Login.as_view(), name='login'),

    # main pages
    path('library/', library.Library.as_view(), name='library'),
    path('player/<uuid:playlist_id>/', player.Player.as_view(), name='play_playlist'),

    # content management pages
    path('manage/', manage.Dashboard.as_view(), name='manage_content'),
    path('playlist/create', manage.ManagePlaylist.as_view(), name='create_playlist'),
    path('upload/', manage.UploadFile.as_view(), name='upload_song'),
    path('scan/', manage.ScanFile.as_view(), name='scan_song'),

    # api 'endpoints'
    path('api/playlists/<uuid:model_id>/', api.SingleView.as_view(),
         {'model': Playlist}, name='playlist_single'),
    path('api/playlists/', api.ListView.as_view(),
         {'model': Playlist}, name='playlist_list'),
    path('api/songs/<uuid:model_id>/', api.SingleView.as_view(),
         {'model': Song}, name='song_single'),
    path('api/songs/', api.ListView.as_view(),
         {'model': Song}, name='song_list'),

    # redirect and catch-all
    path('', RedirectView.as_view(pattern_name='library', permanent=True)),
    # should be a 404 and then redirect
    re_path(r'^player/.*$', RedirectView.as_view(pattern_name='library', permanent=False))
]
