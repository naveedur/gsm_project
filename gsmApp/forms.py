import unicodedata
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django import forms
from.models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from gsmApp import models

from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from allauth.account.forms import SetPasswordField, PasswordField


from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher
from django.contrib.auth.models import User


from django.utils.translation import gettext_lazy as _


class PersonForm(forms.ModelForm):
    class Meta:
        fields = ["title", "Tags"]
        model = models.resource


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']



class UpdateUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email']      


      

