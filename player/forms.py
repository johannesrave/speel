from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField, PasswordInput, ImageField, FileInput, FileField
from tinytag import TinyTag

from player.models import Track, Playlist


class CreateUserForm(UserCreationForm):
    username = CharField(label='Benutzername')
    email = CharField(label='Email Addresse')
    password1 = CharField(label='Passwort', widget=PasswordInput)
    password2 = CharField(label='Passwort bestätigen', widget=PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


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

    class Meta:
        model = Playlist
        fields = ['name', 'tracks', 'image']


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
