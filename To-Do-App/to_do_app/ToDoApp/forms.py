from django import forms
from .models import *
from django.contrib.auth.models import User

# user and  userprofile information forms
class User_Form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('first_name','last_name','username','email','password')

class UserProfileForm(forms.ModelForm):

    class Meta():
        model = UserProfileInformation
        fields = ('phone_number',)

# task form code

class TaskForm(forms.ModelForm):
    class Meta():
        model = Task
        fields = ('title','activity','starting_time', 'reminder_time','status')