from django.urls import path, re_path
from django.views.generic import RedirectView

from player.views import player, login, upload_wizard

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='player', permanent=True)),
    path('login/', login.Login.as_view(), name='login'),
    path('logout/', login.Logout.as_view(), name='logout'),
    path('player/', player.Index.as_view(), name='player'),
    path('player/<uuid:playlist_id>/', player.PlaylistView.as_view(), name='playlist'),
    path('read_file/', upload_wizard.ReadFile.as_view(), name='read file'),
    path('preview_file/', upload_wizard.PreviewFile.as_view(), name='preview file'),
    path('saved_file/', upload_wizard.SavedFile.as_view(), name='saved file'),
    path('song/', player.SongView.as_view(), name='song'),
    re_path(r'^player/.*$', RedirectView.as_view(pattern_name='player', permanent=False))
]
