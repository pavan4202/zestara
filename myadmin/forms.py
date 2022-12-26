from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from users.models import User
from video.models import Video, Classification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(min_length=4,max_length=30,
                               error_messages={
                                   'min_length': 'User name should not be less than 4 characters',
                                   'max_length': 'User name cannot be more than 30 characters',
                                   'required': 'Username can not be empty',
                               },
                               widget=forms.TextInput(attrs={'placeholder': 'please enter user name'}))
    password = forms.CharField(#min_length=8,
        max_length=30,
                               error_messages={
                                   'min_length': 'Password must be no less than 8 characters',
                                   'max_length': 'Password cannot be more than 30 characters',
                                   'required': 'password can not be blank',
                               },
                               widget=forms.PasswordInput(attrs={'placeholder': 'Please enter the password'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    error_messages = {'invalid_login': 'wrong user name or password', }


class VideoPublishForm(forms.ModelForm):
    title = forms.CharField(min_length=4, max_length=200, required=True,
                              error_messages={
                                  'min_length': 'min length is 4 characters',
                                  'max_length': 'max length is 200 characters',
                                  'required': 'Title is required'
                              },
                              widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    desc = forms.CharField(min_length=4, max_length=200, required=True,
                              error_messages={
                                  'min_length': 'min length is 4 characters',
                                  'max_length': 'max length is 200 characters',
                                  'required': 'description is required'
                              },
                              widget=forms.Textarea(attrs={'placeholder': 'description is required'}))
    cover = forms.ImageField(required=True,
                             error_messages={
                                 'required': 'Cover cannot be empty'
                             },
                             widget=forms.FileInput(attrs={'class' : 'n'}))
    status = forms.CharField(min_length=1, max_length=1, required=False,
                             widget=forms.HiddenInput(attrs={'value':'0'}))
    class Meta:
        model = Video
        fields = ['title', 'desc','status', 'cover', 'classification']


class VideoEditForm(forms.ModelForm):
    title = forms.CharField(min_length=4, max_length=200, required=True,
                              error_messages={
                                  'min_length': 'min length is 4 characters',
                                  'max_length': 'max length is 200 characters',
                                  'required': 'Title is required'
                              },
                              widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    desc = forms.CharField(min_length=4, max_length=200, required=True,
                              error_messages={
                                  'min_length': 'min length is 4 characters',
                                  'max_length': 'max length is 200 characters',
                                  'required': 'description is required'
                              },
                              widget=forms.Textarea(attrs={'placeholder': 'Description'}))
    cover = forms.ImageField(required=True,
                             error_messages={
                                 'required': 'cover cannot be empty'
                             },
                             widget=forms.FileInput(attrs={'class' : 'n'}))

    status = forms.CharField(min_length=1,max_length=1,required=False,
                             widget=forms.HiddenInput())

    # classification = forms.ModelChoiceField(queryset=Classification.objects.all())
    # classification = forms.CharField(min_length=1,max_length=1,required=False,
    #                          widget=forms.HiddenInput())

    class Meta:
        model = Video
        fields = ['title', 'desc', 'status', 'cover','classification']



class UserAddForm(forms.ModelForm):
    username = forms.CharField(min_length=4,max_length=30,
                               error_messages={
                                   'min_length': 'min length is 4 characters',
                                   'max_length': 'max length is 30 characters',
                                   'required': 'Username is required'
                               },
                               widget=forms.TextInput(attrs={'placeholder': 'please enter user name'}))
    password = forms.CharField(min_length=8,max_length=30,
                               error_messages={
                                   'min_length': 'min length is 8 characters',
                                   'max_length': 'max length is 30 characters',
                                   'required': 'password is required'
                               },
                               widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    class Meta:
        model = User
        fields = ['username', 'password','is_staff' ]


def username_validate(value):
    if value == "admin":
        raise ValidationError('Cannot edit super administrator')


class UserEditForm(forms.ModelForm):
    username = forms.CharField(min_length=4, max_length=30, required=True,
                               validators=[username_validate],
                              error_messages={
                                  'min_length': 'min length is 4 characters',
                                  'max_length': 'max length is 30 characters',
                                  'required': 'Username is required'
                              },
                              widget=forms.TextInput(attrs={'placeholder': 'username'}))

    class Meta:
        model = User
        fields = ['username','is_staff']


class ClassificationAddForm(forms.ModelForm):
    title = forms.CharField(min_length=2, max_length=30, required=True,
                            error_messages={
                                'min_length': 'min length is 2 characters',
                                'max_length': 'max length is 30 characters',
                                'required': 'title is required'
                            },
                            widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    class Meta:
        model = Classification
        fields = ['title', 'status' ]

class ClassificationEditForm(forms.ModelForm):
    title = forms.CharField(min_length=2, max_length=30, required=True,
                              error_messages={
                                  'min_length': 'min length is 2 characters',
                                  'max_length': 'max length is 30 characters',
                                  'required': 'Title is required'
                              },
                              widget=forms.TextInput(attrs={'placeholder': 'Title'}))

    class Meta:
        model = Classification
        fields = ['title','status']