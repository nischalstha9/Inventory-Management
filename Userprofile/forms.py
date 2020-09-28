from django.forms import ModelForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm

class ProfileUpdateForm(ModelForm):
    
    class Meta:
        model = Profile
        fields = [
            'contact','dp'
        ]
        labels  = {
        'dp':'Profile Picture',
        }

class UserDetailUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name'
        ]

    
class SignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=False)
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)
        

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(SignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # Add your own processing here.

        # You must return the original result.
        return user
