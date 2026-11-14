from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Patient
from apps.medical_history.models import Allergy, ClinicalAlert, MedicalHistory


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'phone', 'email', 'national_id', 'address',
            'emergency_contact_name', 'emergency_contact_phone', 'notes', 'is_active',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'national_id': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-input'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'is_active': forms.CheckboxInput(),
        }


class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ['allergen', 'reaction', 'severity', 'notes', 'is_active']
        widgets = {
            'allergen': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'reaction': forms.TextInput(attrs={'class': 'form-input'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'is_active': forms.CheckboxInput(),
        }


class ClinicalAlertForm(forms.ModelForm):
    class Meta:
        model = ClinicalAlert
        fields = ['title', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'is_active': forms.CheckboxInput(),
        }


class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = [
            'past_medical_history', 'past_surgical_history', 'current_medications',
            'family_history', 'social_history', 'previous_injuries',
            'previous_foot_ankle_treatments',
        ]
        widgets = {f: forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}) for f in [
            'past_medical_history', 'past_surgical_history', 'current_medications',
            'family_history', 'social_history', 'previous_injuries',
            'previous_foot_ankle_treatments',
        ]}
