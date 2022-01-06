from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField, PasswordInput, ImageField, FileInput, FileField, ClearableFileInput
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


class PlaylistForm(ModelForm):
    image = ImageField(required=False, label='Image', widget=FileInput)
    new_tracks = FileField()

    class Meta:
        model = Playlist
        fields = ['name', 'tracks', 'image']


class PlaylistCreateForm(ModelForm):
    image = ImageField(required=False, label='Image', widget=FileInput)
    new_tracks = FileField(
        required=False,
        label='New Tracks',
        widget=ClearableFileInput(attrs={'multiple': True})
    )

    class Meta:
        model = Playlist
        fields = ['name', 'tracks', 'image', 'new_tracks']
        # widgets = {'new_tracks': ClearableFileInput(attrs={'multiple': True})}


class DeleteForm(Form):
    pass


class CreateTrackForm(ModelForm):
    audio_file = FileField(max_length=(1024 * 1024 * 50))

    class Meta:
        model = Track
        fields = ['audio_file']

    def clean_file(self):
        clean_file = self.cleaned_data.get('audio_file')

        if not TinyTag.is_supported(clean_file.name):
            raise ValidationError('Dateiformat wird nicht unterstützt.')

        return clean_file


class UpdateTrackForm(ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'artists']
