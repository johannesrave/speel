from django.urls import path, re_path
from django.views.generic import RedirectView

from player.views import player, login

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='player', permanent=True)),
    path('login/', login.Login.as_view(), name='login'),
    path('logout/', login.Logout.as_view(), name='logout'),
    path('player/', player.Index.as_view(), name='player'),
    path('player/<uuid:playlist>/', player.PlaylistView.as_view(), name='playlist'),
    re_path(r'^.*$', RedirectView.as_view(pattern_name='player', permanent=False), name='redirect_to_home')
]
