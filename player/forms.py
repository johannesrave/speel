from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField, PasswordInput

from player.models import Track, Playlist, TemporaryFile


class LoginForm(Form):
    username = CharField(label='Benutzername')
    password = CharField(label='Passwort', widget=PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not (user and user.is_active):
                raise ValidationError("Benutzername oder Passwort sind nicht korrekt")


class TrackForm(ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'artists']


class PlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'tracks', 'thumbnail_file']


class TemporaryFileForm(ModelForm):
    class Meta:
        model = TemporaryFile
        fields = ['file']
