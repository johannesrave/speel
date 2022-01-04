from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField, PasswordInput, ImageField, FileInput
from tinytag import TinyTag

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
    image = ImageField(required=False, label='Image', widget=FileInput)

    class Meta:
        model = Playlist
        fields = ['name', 'tracks', 'image']


class TemporaryFileForm(ModelForm):
    class Meta:
        model = TemporaryFile
        fields = ['file']

    def clean_file(self):
        clean_file = self.cleaned_data.get('file')

        if not TinyTag.is_supported(clean_file.name):
            raise ValidationError('Dateiformat wird nicht unterstützt.')

        if not clean_file.size < 1024 * 1024 * 50:
            raise ValidationError('Datei ist größer als 50MB.')

        return clean_file
