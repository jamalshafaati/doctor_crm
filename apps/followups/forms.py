from django import forms
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.patients.models import Patient
from apps.surgery.models import Surgery
from apps.core.dates import parse_jalali_date
from .models import FollowUp


class FollowUpForm(forms.ModelForm):
    scheduled_date_j = forms.CharField(
        required=True, label=_('تاریخ پیگیری (شمسی)'),
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '1403/08/23'})
    )
    next_followup_date_j = forms.CharField(
        required=False, label=_('پیگیری بعدی (شمسی)'),
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '1403/09/01'})
    )

    class Meta:
        model = FollowUp
        fields = [
            'patient', 'surgery', 'doctor', 'status', 'side',
            'pain_score', 'wound_status', 'mobility', 'weight_bearing_status',
            'rehabilitation_progress', 'complications', 'assessment_notes',
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'surgery': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'side': forms.Select(attrs={'class': 'form-select'}),
            'pain_score': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 10}),
            'wound_status': forms.TextInput(attrs={'class': 'form-input'}),
            'mobility': forms.TextInput(attrs={'class': 'form-input'}),
            'weight_bearing_status': forms.TextInput(attrs={'class': 'form-input'}),
            'rehabilitation_progress': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'complications': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'assessment_notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.filter(is_active=True).order_by('last_name')
        self.fields['doctor'].queryset = User.objects.filter(role__in=['doctor', 'admin'], is_active=True)
        self.fields['surgery'].queryset = Surgery.objects.select_related('patient').order_by('-surgery_date')[:100]
        self.fields['surgery'].required = False
        self.fields['patient'].label_from_instance = lambda o: f"{o.patient_number} — {o.full_name}"
        self.fields['doctor'].label_from_instance = lambda o: o.get_full_name() or o.username
        self.fields['surgery'].label_from_instance = lambda o: f"{o.procedure} — {o.patient.full_name}"
        if self.instance and self.instance.pk:
            from apps.core.dates import to_jalali
            if self.instance.scheduled_date:
                self.fields['scheduled_date_j'].initial = to_jalali(self.instance.scheduled_date)
            if self.instance.next_followup_date:
                self.fields['next_followup_date_j'].initial = to_jalali(self.instance.next_followup_date)

    def clean_scheduled_date_j(self):
        val = self.cleaned_data.get('scheduled_date_j')
        d = parse_jalali_date(val)
        if not d:
            raise forms.ValidationError(_('تاریخ شمسی معتبر وارد کنید (مثال: 1403/08/23)'))
        return d

    def clean_next_followup_date_j(self):
        val = self.cleaned_data.get('next_followup_date_j')
        if not val:
            return None
        d = parse_jalali_date(val)
        if not d:
            raise forms.ValidationError(_('تاریخ نامعتبر'))
        return d

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.scheduled_date = self.cleaned_data['scheduled_date_j']
        obj.next_followup_date = self.cleaned_data.get('next_followup_date_j')
        if commit:
            obj.save()
        return obj
