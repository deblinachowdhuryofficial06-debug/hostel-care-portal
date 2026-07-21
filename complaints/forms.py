from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Complaint, Comment


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False  # 🌟 Ensures user is a student
        user.is_superuser = False
        if commit:
            user.save()
        return user


class WardenRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # 🌟 Ensures user is a warden
        if commit:
            user.save()
        return user


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['room_number', 'title', 'description']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 102-A'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief title of the issue'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the problem in detail'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a response...'}),
        }