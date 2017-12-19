from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.files import File
from ask.models import *
from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your login here', }),
        max_length=30
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*******', }),
    )

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('login', ''), password=data.get('password', ''))

        if user is not None:
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError('User is not active')
        else:
            raise forms.ValidationError('Wrong login or password')

class AnswerForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control answer-textarea',
                                     'placeholder': "Enter your answer here.", 'rows': "6" })
    )

    def save(self, question, user):
        data = self.cleaned_data
        answer = Answer(text = data.get('text'), author = user, question = question)
        answer.save()

class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={ 'class': 'form-control' }),
        max_length=30
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={ 'class': 'form-control' }),
        max_length=100
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={ 'class': 'form-control', 'placeholder': '********' }),
        min_length=8
    )
    password_repeat = forms.CharField(
        label='Repeat Password',
        widget=forms.PasswordInput(attrs={ 'class': 'form-control', 'placeholder': '********' }),
        min_length=8
    )
    avatar = forms.FileField(
        label='Avatar',
        widget=forms.ClearableFileInput(),
        required=False
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError('Username is already used')
        except User.DoesNotExist:
            return username

    def clean_password_repeat(self):
        pswd = self.cleaned_data.get('password', '')
        pswd_repeat = self.cleaned_data.get('password_repeat', '')

        if pswd != pswd_repeat:
            raise forms.ValidationError('Passwords does not matched')
        return pswd_repeat

    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        try:
            e = User.objects.get(email=email)
            raise forms.ValidationError('Email is already used')
        except User.DoesNotExist:
            return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar is not None:
            if 'image' not in avatar.content_type:
                raise forms.ValidationError('Wrong image type')
        return avatar

    def save(self):
        data = self.cleaned_data
        password = data.get('password')
        newUser = User()
        newUser.username = data.get('username')
        newUser.password = make_password(password)
        newUser.email = data.get('email')
        newUser.is_active = True
        newUser.is_superuser = False
        newUser.save()
        newUser.rating = 0
        if data.get('avatar') is not None:
            avatar = data.get('avatar')
            newUser.avatar.save('%s_%s' % (newUser.username, avatar.name), avatar, save=True)
            newUser.save()
        return authenticate(username=newUser.username, password=password)


class QuestionForm(forms.Form):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100
    )
    text = forms.CharField(
        label='Text',
        widget=forms.Textarea(
            attrs={'class': 'form-control noresize', 'rows': '15' }),
        max_length=1000
    )
    tags = forms.CharField(
        label='Tags',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tag1,Tag2,Tag3'}),
        required=False
    )
