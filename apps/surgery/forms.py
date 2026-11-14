from django import forms
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.patients.models import Patient
from .models import Surgery, Implant


class SurgeryForm(forms.ModelForm):
    class Meta:
        model = Surgery
        fields = [
            'patient', 'surgeon', 'procedure', 'surgery_date', 'status', 'side',
            'preoperative_diagnosis', 'postoperative_diagnosis', 'indication',
            'procedure_description', 'anesthesia', 'complications',
            'postoperative_instructions', 'surgical_notes',
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'surgeon': forms.Select(attrs={'class': 'form-select'}),
            'procedure': forms.TextInput(attrs={'class': 'form-input'}),
            'surgery_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'side': forms.Select(attrs={'class': 'form-select'}),
            'preoperative_diagnosis': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'postoperative_diagnosis': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'indication': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'procedure_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'anesthesia': forms.TextInput(attrs={'class': 'form-input'}),
            'complications': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'postoperative_instructions': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'surgical_notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.filter(is_active=True).order_by('last_name')
        self.fields['surgeon'].queryset = User.objects.filter(role='doctor', is_active=True)
        self.fields['patient'].label_from_instance = lambda o: f"{o.patient_number} — {o.full_name}"
        self.fields['surgeon'].label_from_instance = lambda o: o.get_full_name() or o.username


class ImplantForm(forms.ModelForm):
    class Meta:
        model = Implant
        fields = ['name', 'manufacturer', 'catalog_number', 'size', 'quantity', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-input'}),
            'catalog_number': forms.TextInput(attrs={'class': 'form-input'}),
            'size': forms.TextInput(attrs={'class': 'form-input'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }
