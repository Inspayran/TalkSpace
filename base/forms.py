from django import forms
from django.contrib.auth.models import User

from accounts.models import MyUser
from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants', ]


class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput, required=False)
    # confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', required=False)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'bio', 'avatar', ]

    # def clean_confirm_password(self):
    #     password = self.cleaned_data.get('password')
    #     confirm_password = self.cleaned_data.get('confirm_password')
    #     if password and confirm_password and password != confirm_password:
    #         raise forms.ValidationError('Passwords do not match.')
    #     return confirm_password
