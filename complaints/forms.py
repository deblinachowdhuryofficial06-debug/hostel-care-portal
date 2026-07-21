from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Complaint

# --- ORIGINAL COMPLAINT FORM ---
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'room_number', 'image']


# --- NEW CUSTOM REGISTRATION FORMS ---
class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False  # 🌟 MUST BE FALSE for regular students!
        if commit:
            user.save()
        return user
class WardenRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': f'Enter {field_name}'})
            field.help_text = None 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user