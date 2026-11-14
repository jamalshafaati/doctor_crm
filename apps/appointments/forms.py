from django import forms
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.patients.models import Patient
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'scheduled_at', 'duration_minutes', 'reason', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_at': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-input', 'min': 10, 'step': 5}),
            'reason': forms.TextInput(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.filter(is_active=True).order_by('last_name')
        self.fields['doctor'].queryset = User.objects.filter(role='doctor', is_active=True)
        self.fields['patient'].label_from_instance = lambda obj: f"{obj.patient_number} — {obj.full_name}"
        self.fields['doctor'].label_from_instance = lambda obj: obj.get_full_name() or obj.username
