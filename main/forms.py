from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'image', 'category_id', )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-text'}),
            'content': forms.Textarea(attrs={'class': 'form-text'}),
            'image': forms.FileInput(attrs={'class': 'form-text'}),
            'category_id': forms.Select(attrs={'class': 'form-text'}),
        }

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    secret_word = forms.CharField(
        label='Секретное слово',
        widget = forms.TextInput(attrs={'class':'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget = forms.TextInput(attrs={'class':'form-control'})
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

    secret_word = forms.CharField(
        label='Секретное слово',
        widget = forms.TextInput(attrs={'class':'form-control'})
    )

