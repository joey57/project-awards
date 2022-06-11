from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Projects

class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['username', 'email']  

class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['image']

class CreateProfileForm(forms.ModelForm):  
    class Meta:
        model = Profile
        exclude = ['user']

class UpdateProfile(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['image', 'name', 'bio'] 

class NewSiteForm(forms.ModelForm):
  class Meta:
    model = Projects
    exclude = ['profile', 'user', 'pub_date', 'voters']
