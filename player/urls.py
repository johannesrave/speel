from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from player.models import Audiobook, Track
from player.views import player, api, library, manage
from player.views.manage import account, audiobook

urlpatterns = [
    # account pages
    path('account/login/', manage.account.Login.as_view(), name='login'),
    path('account/register/', manage.account.Register.as_view(), name='register'),
    path('account/', account.UpdateAccount.as_view(), name='account'),

    path('account/password/reset/', name='password_reset',
         view=auth_views.PasswordResetView.as_view(
             template_name='forms/password-reset.html',
             success_url=reverse_lazy('password_reset_sent'))),

    path('account/password/reset/sent/', name='password_reset_sent',
         view=auth_views.PasswordResetDoneView.as_view(
             template_name='pages/password-reset-sent.html')),

    path('account/password/reset/<uidb64>/<token>', name='password_reset_confirm',
         view=auth_views.PasswordResetConfirmView.as_view(
             template_name='forms/password-reset-confirm.html',
             success_url=reverse_lazy('password_reset_complete'))),

    path('account/password/reset/complete/', name='password_reset_complete',
         view=auth_views.PasswordResetCompleteView.as_view(
             template_name='pages/password-reset-complete.html')),

    # player pages ('kids' pages)
    path('library/', library.ViewLibrary.as_view(), name='library'),
    path('audiobooks/', library.EditLibrary.as_view(), name='audiobooks'),
    path('player/', RedirectView.as_view(pattern_name='library', permanent=False)),
    path('player/<uuid:audiobook_id>/', player.Player.as_view(), name='play_audiobook'),

    # content management pages ('parents' pages)
    path('audiobooks/new/', manage.audiobook.CreateAudiobook.as_view(),
         name='create_audiobook'),
    path('audiobooks/<uuid:audiobook_id>/edit/', manage.audiobook.UpdateAudiobook.as_view(),
         name='update_audiobook'),
    path('audiobooks/<uuid:audiobook_id>/delete/', manage.audiobook.DeleteAudiobook.as_view(),
         name='delete_audiobook'),

    # HTTP-api 'endpoints'
    path('api/audiobooks/<uuid:model_id>/', api.SingleView.as_view(),
         {'model': Audiobook}, name='audiobook_single'),
    path('api/audiobooks/', api.ListView.as_view(),
         {'model': Audiobook}, name='audiobook_list'),
    # path('api/tracks/<uuid:model_id>/', api.SingleView.as_view(),
    #      {'model': Track}, name='track_single'),
    # path('api/tracks/', api.ListView.as_view(),
    #      {'model': Track}, name='track_list'),

    # redirect and catch-all
    path('', RedirectView.as_view(pattern_name='library', permanent=False)),
]
