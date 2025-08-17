from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import myUser
from .models import Meetop

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = myUser
        fields = ['name', 'email', 'mobile_number', 'birth_date', 'gender', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


# MeetopCreation
class MeetopForm(forms.ModelForm):
    class Meta:
        model = Meetop
        fields = ['title', 'state', 'from_date', 'meetup_date', 'description', 'to_date', 'meetup_time', 'address', 'activate', 'image']



