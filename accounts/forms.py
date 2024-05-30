from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'country', 'gender']
        labels = {
            "profile_pic": "",
            "country": "",
            "gender": ""
        }
