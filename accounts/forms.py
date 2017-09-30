from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from accounts import models
from django import forms
from betterforms.multiform import MultiModelForm, MultiForm


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"

class UserUpdateForm(forms.ModelForm):
    class Meta:
        fields= ('fav_team',)
        model = models.UserProfile

class UserCreationMultiForm(MultiModelForm):
    form_classes = {
        'user': UserCreateForm,
        'profile': UserUpdateForm,
    }
    def save(self, commit=True):
        objects = super(UserCreationMultiForm, self).save(commit=False)

        if commit:
            user = objects['user']
            user.save()
            profile = objects['profile']
            profile.UserProfile = user
            profile.save()

        return objects
