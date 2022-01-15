from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField, PasswordInput, ImageField, FileInput, FileField, \
    ClearableFileInput, TextInput, EmailField

from player.models import Audiobook, User


class CreateUserForm(UserCreationForm):
    username = CharField(max_length=100, required=True, label='Benutzername',
                         widget=TextInput(attrs={'class': 'form-control'}))
    email = EmailField(required=True, label='Email Addresse',
                       widget=TextInput(attrs={'class': 'form-control'}))
    password1 = CharField(max_length=100, required=True, label='Passwort',
                          widget=PasswordInput())
    password2 = CharField(max_length=100, required=True, label='Passwort bestätigen',
                          widget=PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUserForm(ModelForm):
    username = CharField(max_length=100, required=True,
                         label='Benutzername', widget=TextInput(attrs={'class': 'form-control'}))
    email = EmailField(required=True, label='Email Addresse',
                       widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


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


class UpdateAudiobookForm(ModelForm):
    image = ImageField(required=False, label='Image', widget=FileInput)
    new_tracks = FileField(required=False)

    class Meta:
        model = Audiobook
        fields = ['name', 'image']


class CreateAudiobookForm(ModelForm):
    image = ImageField(required=False, label='Cover', widget=FileInput)
    new_tracks = FileField(
        required=False,
        label='Tracks',
        widget=ClearableFileInput(attrs={'multiple': True}),
        max_length=(1024 * 1024 * 50)
    )

    class Meta:
        model = Audiobook
        fields = ['name', 'image', 'new_tracks']
