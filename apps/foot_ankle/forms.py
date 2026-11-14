from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (
    TraumaExam, SportsExam, AchillesExam, FlatfootExam,
    DeformityExam, ArthritisExam, AnatomyFinding
)
from apps.clinical.models import ClinicalExamination, Side


class ClinicalExaminationForm(forms.ModelForm):
    class Meta:
        model = ClinicalExamination
        fields = [
            'chief_complaint', 'onset', 'duration', 'mechanism_of_injury',
            'pain_location', 'pain_severity', 'pain_character',
            'aggravating_factors', 'relieving_factors', 'functional_limitations',
            'previous_treatment', 'inspection', 'palpation', 'range_of_motion',
            'stability', 'muscle_strength', 'neurovascular', 'gait',
            'functional_assessment', 'side', 'notes',
        ]
        widgets = {f: forms.TextInput(attrs={'class': 'form-input'}) for f in [
            'onset', 'duration', 'pain_location', 'pain_character'
        ]}
        widgets.update({
            'chief_complaint': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'mechanism_of_injury': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'aggravating_factors': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'relieving_factors': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'functional_limitations': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'previous_treatment': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'inspection': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'palpation': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'range_of_motion': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'stability': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'muscle_strength': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'neurovascular': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'gait': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'functional_assessment': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'pain_severity': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 10}),
            'side': forms.Select(attrs={'class': 'form-select'}),
        })


class TraumaExamForm(forms.ModelForm):
    class Meta:
        model = TraumaExam
        fields = [
            'injury_date', 'mechanism', 'side', 'location', 'weight_bearing',
            'swelling', 'bruising', 'deformity', 'tenderness',
            'neurovascular_status', 'imaging_findings',
            'weber_class', 'lauge_hansen', 'ao_ota', 'notes',
        ]
        widgets = {
            'injury_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'mechanism': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'side': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'weight_bearing': forms.TextInput(attrs={'class': 'form-input'}),
            'swelling': forms.TextInput(attrs={'class': 'form-input'}),
            'bruising': forms.TextInput(attrs={'class': 'form-input'}),
            'deformity': forms.TextInput(attrs={'class': 'form-input'}),
            'tenderness': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'neurovascular_status': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'imaging_findings': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'weber_class': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'A / B / C'}),
            'lauge_hansen': forms.TextInput(attrs={'class': 'form-input'}),
            'ao_ota': forms.TextInput(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }


class AchillesExamForm(forms.ModelForm):
    class Meta:
        model = AchillesExam
        fields = [
            'condition_type', 'side', 'pain_location', 'duration',
            'tendon_tenderness', 'tendon_thickening', 'palpable_defect',
            'thompson_test', 'single_leg_heel_raise', 'plantarflexion_strength',
            'imaging_findings', 'previous_treatment', 'notes',
        ]
        widgets = {
            'condition_type': forms.Select(attrs={'class': 'form-select'}),
            'side': forms.Select(attrs={'class': 'form-select'}),
            'pain_location': forms.TextInput(attrs={'class': 'form-input'}),
            'duration': forms.TextInput(attrs={'class': 'form-input'}),
            'tendon_tenderness': forms.CheckboxInput(),
            'tendon_thickening': forms.CheckboxInput(),
            'palpable_defect': forms.CheckboxInput(),
            'thompson_test': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Positive / Negative'}),
            'single_leg_heel_raise': forms.TextInput(attrs={'class': 'form-input'}),
            'plantarflexion_strength': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 5}),
            'imaging_findings': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'previous_treatment': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }


class SportsExamForm(forms.ModelForm):
    class Meta:
        model = SportsExam
        fields = [
            'sport_type', 'activity_level', 'mechanism', 'previous_injuries', 'side',
            'instability', 'atfl', 'cfl', 'ptfl', 'syndesmosis',
            'anterior_drawer', 'talar_tilt', 'squeeze_test', 'external_rotation_test',
            'functional_tests', 'return_to_sport', 'notes',
        ]
        widgets = {
            'sport_type': forms.TextInput(attrs={'class': 'form-input'}),
            'activity_level': forms.TextInput(attrs={'class': 'form-input'}),
            'mechanism': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'previous_injuries': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'side': forms.Select(attrs={'class': 'form-select'}),
            'instability': forms.CheckboxInput(),
            'atfl': forms.TextInput(attrs={'class': 'form-input'}),
            'cfl': forms.TextInput(attrs={'class': 'form-input'}),
            'ptfl': forms.TextInput(attrs={'class': 'form-input'}),
            'syndesmosis': forms.TextInput(attrs={'class': 'form-input'}),
            'anterior_drawer': forms.TextInput(attrs={'class': 'form-input'}),
            'talar_tilt': forms.TextInput(attrs={'class': 'form-input'}),
            'squeeze_test': forms.TextInput(attrs={'class': 'form-input'}),
            'external_rotation_test': forms.TextInput(attrs={'class': 'form-input'}),
            'functional_tests': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'return_to_sport': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }


class FlatfootExamForm(forms.ModelForm):
    class Meta:
        model = FlatfootExam
        fields = [
            'side', 'flexibility', 'arch_height', 'hindfoot_alignment',
            'forefoot_abduction', 'heel_rise', 'jack_test', 'single_heel_rise',
            'ptt_assessment', 'weight_bearing_xray', 'mearys_angle', 'calcaneal_pitch', 'notes',
        ]
        widgets = {
            'side': forms.Select(attrs={'class': 'form-select'}),
            'flexibility': forms.Select(attrs={'class': 'form-select'}),
            'arch_height': forms.TextInput(attrs={'class': 'form-input'}),
            'hindfoot_alignment': forms.TextInput(attrs={'class': 'form-input'}),
            'forefoot_abduction': forms.TextInput(attrs={'class': 'form-input'}),
            'heel_rise': forms.TextInput(attrs={'class': 'form-input'}),
            'jack_test': forms.TextInput(attrs={'class': 'form-input'}),
            'single_heel_rise': forms.TextInput(attrs={'class': 'form-input'}),
            'ptt_assessment': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'weight_bearing_xray': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'mearys_angle': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1'}),
            'calcaneal_pitch': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }


class DeformityExamForm(forms.ModelForm):
    class Meta:
        model = DeformityExam
        fields = [
            'deformity_type', 'side', 'location', 'flexible_or_rigid',
            'severity', 'progression', 'functional_impact',
            'associated_deformities', 'imaging_measurements', 'notes',
        ]
        widgets = {
            'deformity_type': forms.Select(attrs={'class': 'form-select'}),
            'side': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'flexible_or_rigid': forms.TextInput(attrs={'class': 'form-input'}),
            'severity': forms.TextInput(attrs={'class': 'form-input'}),
            'progression': forms.TextInput(attrs={'class': 'form-input'}),
            'functional_impact': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'associated_deformities': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'imaging_measurements': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }


class ArthritisExamForm(forms.ModelForm):
    class Meta:
        model = ArthritisExam
        fields = [
            'joint', 'side', 'pain', 'stiffness', 'morning_stiffness',
            'swelling', 'rom', 'functional_limitation',
            'imaging_findings', 'takakura_stage', 'notes',
        ]
        widgets = {
            'joint': forms.TextInput(attrs={'class': 'form-input'}),
            'side': forms.Select(attrs={'class': 'form-select'}),
            'pain': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 10}),
            'stiffness': forms.TextInput(attrs={'class': 'form-input'}),
            'morning_stiffness': forms.TextInput(attrs={'class': 'form-input'}),
            'swelling': forms.TextInput(attrs={'class': 'form-input'}),
            'rom': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'functional_limitation': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'imaging_findings': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'takakura_stage': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '1–4'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }


class AnatomyFindingForm(forms.ModelForm):
    class Meta:
        model = AnatomyFinding
        fields = ['view', 'region', 'side', 'finding_type', 'severity', 'notes', 'coord_x', 'coord_y']
        widgets = {
            'view': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.TextInput(attrs={'class': 'form-input'}),
            'side': forms.Select(attrs={'class': 'form-select'}),
            'finding_type': forms.Select(attrs={'class': 'form-select'}),
            'severity': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 5}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'coord_x': forms.HiddenInput(),
            'coord_y': forms.HiddenInput(),
        }
