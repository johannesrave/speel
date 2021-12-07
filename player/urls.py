from django.urls import path, re_path
from django.views.generic import RedirectView

from player.views import player, login, upload_wizard

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='player', permanent=True)),
    path('login/', login.Login.as_view(), name='login'),
    path('logout/', login.Logout.as_view(), name='logout'),
    path('player/', player.Index.as_view(), name='player'),
    path('player/<uuid:playlist_id>/', player.PlaylistView.as_view(), name='playlist'),
    path('upload/', upload_wizard.UploadFile.as_view(), name='upload_song'),
    path('scan/', upload_wizard.ScanFile.as_view(), name='scan_song'),
    path('song/', player.SongView.as_view(), name='song'),
    re_path(r'^player/.*$', RedirectView.as_view(pattern_name='player', permanent=False))
]
