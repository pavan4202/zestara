from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import User, Feedback


def avatar_file_size(value):
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('The avatar file is too large, please limit it to 2MB')

class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(min_length=1,max_length=20,required=False,
                               error_messages={
                                   'min_length':'Nickname is at least 4 characters',
                                   'min_length':'Nickname cannot be more than 20 characters',
                               },
                               widget=forms.TextInput())
    avatar = forms.ImageField(required=False, validators=[avatar_file_size],
                              widget=forms.FileInput(attrs={'class' : 'n'}))
    email = forms.EmailField(required=True,
                             error_messages={
                                 'invalid': 'Please enter a valid email address',
                             },
                             widget=forms.EmailInput())
    gender = forms.CharField(min_length=1,max_length=1,required=False,
                             widget=forms.HiddenInput())

    mobile = forms.CharField(min_length=10,max_length=10,required=False,
                             error_messages={
                                 'min_length':'Please enter an 11-digit mobile phone number',
                                 'max_length':'Please enter 11-digit mobile phone number',
                             },
                             widget=forms.NumberInput())

    class Meta:
        model = User
        fields = ['nickname', 'avatar', 'email', 'gender', 'mobile']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(min_length=4,max_length=30,
                               error_messages={
                                   'min_length':'User name is not less than 4 characters',
                                   'max_length':'User name cannot be more than 30 characters',
                                   'required':'User name cannot be empty',
                               },
                               widget=forms.TextInput(attrs={'placeholder': 'please enter user name'}))
    password = forms.CharField(min_length = 4, max_length=30,
                               error_messages={
                                   'min_length':'Password is cannot be less than 8 characters',
                                   'max_length':'Password cannot be more than 30 characters',
                                   'required':'Password cannot be empty',
                               },
                               widget=forms.PasswordInput(attrs={'placeholder': 'Please enter the password'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    error_messages = {'invalid_login': 'wrong user name or password', }


class SignUpForm(UserCreationForm):
    username = forms.CharField(min_length=4,max_length=30,
                               error_messages={
                                   'min_length':'User name is not less than 4 characters',
                                   'max_length':'User name cannot be more than 30 characters',
                                   'required':'User name cannot be empty',
                               },
                               widget=forms.TextInput(attrs={'placeholder': 'please enter user name'}))
    password1 = forms.CharField(min_length=4, max_length=30,
                                error_messages={
                                    'min_length':'Password is not less than 8 characters',
                                    'max_length':'Password cannot be more than 30 characters',
                                    'required':'Password cannot be empty',
                                },
                                widget=forms.PasswordInput(attrs={'placeholder': 'Please enter the password'}))
    password2 = forms.CharField(min_length=4,max_length=30,
                                error_messages={
                                    'min_length':'Password is not less than 8 characters',
                                    'max_length':'Password cannot be more than 30 characters',
                                    'required':'Password cannot be empty',
                                },
                                widget=forms.PasswordInput(attrs={'placeholder': 'Please confirm your password'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)

    error_messages = {'password_mismatch': 'The two passwords are inconsistent', }


class ChangePwdForm(PasswordChangeForm):
    old_password = forms.CharField(error_messages={'required':'Cannot be empty',},
        widget=forms.PasswordInput(attrs={'placeholder':'Please enter the old password'})
    )
    new_password1 = forms.CharField(error_messages={'required':'Cannot be empty',},
        widget=forms.PasswordInput(attrs={'placeholder':'Please enter a new password'})
    )
    new_password2 = forms.CharField(error_messages={'required':'Cannot be empty',},
        widget=forms.PasswordInput(attrs={'placeholder':'Please enter the confirmation password'})
    )

class SubscribeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['subscribe']


class FeedbackForm(forms.ModelForm):
    content = forms.CharField(min_length=4,max_length=200,
                               error_messages={
                                   'min_length':'At least 4 characters',
                                   'max_length':'Cannot be more than 200 characters',
                                   'required':'Content cannot be empty'
                               },
                               widget=forms.Textarea(attrs={'placeholder': 'Please enter content'}))
    contact = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder':'Please enter contact information'}))
    class Meta:
        model = Feedback
        fields = ['content', 'contact']
