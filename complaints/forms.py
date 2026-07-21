from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Complaint

# --- ORIGINAL COMPLAINT FORM ---
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'room_number', 'image']


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False  # 🌟 Regular student
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
        user.is_staff = True  # 🌟 Warden privileges
        if commit:
            user.save()
        return user