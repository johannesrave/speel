from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField, PasswordInput, ImageField, FileInput, FileField, ClearableFileInput

from player.models import Playlist


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


class UpdatePlaylistForm(ModelForm):
    image = ImageField(required=False, label='Image', widget=FileInput)
    new_tracks = FileField(required=False)

    class Meta:
        model = Playlist
        fields = ['name', 'image']


class CreatePlaylistForm(ModelForm):
    image = ImageField(required=False, label='Image', widget=FileInput)
    new_tracks = FileField(
        required=False,
        label='New Tracks',
        widget=ClearableFileInput(attrs={'multiple': True}),
        max_length=(1024 * 1024 * 50)
    )

    class Meta:
        model = Playlist
        fields = ['name', 'image', 'new_tracks']


# class CreateTrackForm(ModelForm):
#     test = CharField()
#     test_file = FileField()
#     audio_file = FileField(max_length=(1024 * 1024 * 50))
#
#     class Meta:
#         model = Track
#         fields = ['test', 'test_file', 'audio_file']
#
#     def clean_file(self):
#         clean_file = self.cleaned_data.get('audio_file')
#
#         if not TinyTag.is_supported(clean_file.name):
#             raise ValidationError('Dateiformat wird nicht unterstützt.')
#
#         return clean_file
