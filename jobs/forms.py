from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # Only include fields from the UserProfile model
        fields = ['bio', 'resume',  'experience_level', 'skills', 'location', 'profile_picture']


class UserUpdateForm(forms.ModelForm):
    """
    Form to update built-in User fields: username, first name, last name, and email.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
