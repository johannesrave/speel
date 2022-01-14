from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

from player.models import Playlist, Track
from player.views import player, login, register, api, library, manage
from player.views.manage import account, playlist

urlpatterns = [
    # account pages
    path('login/', login.Login.as_view(), name='login'),
    path('register/', register.Register.as_view(), name='register'),
    path('account/', account.UpdateAccount.as_view(), name='account'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='forms/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='pages/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # player pages ('kids' pages)
    path('library/', library.ViewLibrary.as_view(), name='library'),
    path('playlists/', library.EditLibrary.as_view(), name='playlists'),
    path('player/', RedirectView.as_view(pattern_name='library', permanent=False)),
    path('player/<uuid:playlist_id>/', player.Player.as_view(), name='play_playlist'),

    # content management pages ('parents' pages)
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
