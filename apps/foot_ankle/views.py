from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext as _
from apps.encounters.models import Encounter
from apps.clinical.models import ClinicalExamination
from .forms import (
    ClinicalExaminationForm, TraumaExamForm, AchillesExamForm, SportsExamForm,
    FlatfootExamForm, DeformityExamForm, ArthritisExamForm, AnatomyFindingForm,
)
from .models import (
    TraumaExam, AchillesExam, SportsExam, FlatfootExam,
    DeformityExam, ArthritisExam, AnatomyFinding,
)

FORM_MAP = {
    'clinical': (ClinicalExaminationForm, ClinicalExamination),
    'trauma': (TraumaExamForm, TraumaExam),
    'achilles': (AchillesExamForm, AchillesExam),
    'sports': (SportsExamForm, SportsExam),
    'flatfoot': (FlatfootExamForm, FlatfootExam),
    'deformity': (DeformityExamForm, DeformityExam),
    'arthritis': (ArthritisExamForm, ArthritisExam),
    'anatomy': (AnatomyFindingForm, AnatomyFinding),
}


def _is_clinician(user):
    return user.is_authenticated and (user.is_doctor or user.role == 'admin')


@login_required
def add_exam(request, encounter_id, exam_type):
    if not _is_clinician(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')

    enc = get_object_or_404(Encounter, pk=encounter_id)
    if enc.is_locked:
        messages.error(request, _('این ویزیت نهایی شده و قابل ویرایش نیست.'))
        # Stay on relevant tab after save
    tab_map = {
        'clinical': 'exam', 'trauma': 'specialty', 'achilles': 'specialty',
        'sports': 'specialty', 'flatfoot': 'specialty', 'deformity': 'specialty',
        'arthritis': 'specialty', 'anatomy': 'anatomy',
    }
    tab = tab_map.get(exam_type, 'specialty')
    return redirect(f"/encounters/{enc.pk}/?tab={tab}")

    if exam_type not in FORM_MAP:
        messages.error(request, _('نوع معاینه نامعتبر است.'))
        # Stay on relevant tab after save
    tab_map = {
        'clinical': 'exam', 'trauma': 'specialty', 'achilles': 'specialty',
        'sports': 'specialty', 'flatfoot': 'specialty', 'deformity': 'specialty',
        'arthritis': 'specialty', 'anatomy': 'anatomy',
    }
    tab = tab_map.get(exam_type, 'specialty')
    return redirect(f"/encounters/{enc.pk}/?tab={tab}")

    FormClass, ModelClass = FORM_MAP[exam_type]

    if request.method == 'POST':
        data = request.POST.copy()
        # Normalize checkbox booleans
        for bool_field in ('tendon_tenderness', 'tendon_thickening', 'palpable_defect', 'instability'):
            if bool_field in FormClass.base_fields:
                data[bool_field] = bool_field in request.POST
        form = FormClass(data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.encounter = enc
            obj.save()
            messages.success(request, _('معاینه با موفقیت ثبت شد.'))
        else:
            for field, errors in form.errors.items():
                for err in errors:
                    messages.error(request, f'{field}: {err}')
    # Stay on relevant tab after save
    tab_map = {
        'clinical': 'exam', 'trauma': 'specialty', 'achilles': 'specialty',
        'sports': 'specialty', 'flatfoot': 'specialty', 'deformity': 'specialty',
        'arthritis': 'specialty', 'anatomy': 'anatomy',
    }
    tab = tab_map.get(exam_type, 'specialty')
    return redirect(f"/encounters/{enc.pk}/?tab={tab}")
