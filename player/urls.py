from django.urls import path, re_path
from django.views.generic import RedirectView

from player.views import player, login, upload

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='player', permanent=True)),
    path('login/', login.Login.as_view(), name='login'),
    path('player/', player.Player.as_view(), name='player'),
    path('playlist/create', player.PlaylistCreateView.as_view(), name='create_playlist'),
    path('playlist/<uuid:playlist_id>/', player.PlaylistView.as_view(), name='playlist_to_play'),
    path('upload/', upload.UploadFile.as_view(), name='upload_song'),
    path('scan/', upload.ScanFile.as_view(), name='scan_song'),
    re_path(r'^player/.*$', RedirectView.as_view(pattern_name='player', permanent=False))
]
