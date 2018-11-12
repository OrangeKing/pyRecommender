from django import forms
from django.contrib.auth.models import User

from .models import Post


class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'contents',
            'location',
            'movie'
        ]

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email'
        ]
