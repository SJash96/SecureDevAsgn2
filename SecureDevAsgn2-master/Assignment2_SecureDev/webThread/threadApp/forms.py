from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import datetime

from .models import Threads

class UniqueUserEmailField(forms.EmailField):
    def validate(self, value):
        super(forms.EmailField, self).validate(value)
        try:
            User.objects.get(email = value)
            raise forms.ValidationError("Email already exists")
        except User.MultipleObjectsReturned:
            raise forms.ValidationError("Email already exists")
        except User.DoesNotExist:
            pass


class ExtendedUserCreationForm(UserCreationForm):  
    username = forms.CharField(required = False, max_length = 30)
    email = UniqueUserEmailField(required = True, label = 'Email address')
    first_name = forms.CharField(required = True, max_length = 30)
    last_name = forms.CharField(required = True, max_length = 30)
        
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit)
        if user:
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()
        return user
    
class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = {
            'first_name',
            'last_name',
            'email'
        }

expire_time = [
    ('10 mins', '10 Minutes'),
    ('1 hr', '1 Hour'),
    ('1 day', '1 Day'),
    ('1 week', '1 Week'),
]

expose = [
    ('public', 'Public'),
    ('private', 'Private'),
]

class CreateThreadForm(forms.ModelForm):

    class Meta:
        model = Threads
        fields = ['thread_Name', 'thread_Body', 'thread_Exposer', 'thread_Expire', 'thread_Share', 'created_At']
        widgets = {
            'thread_Body' : forms.Textarea,
            'thread_Exposer' : forms.Select(choices=expose),
            'thread_Expire' : forms.Select(choices=expire_time)
        }