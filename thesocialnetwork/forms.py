from django import forms
from .models import UserProfile

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('about', 'dob', 'image')
