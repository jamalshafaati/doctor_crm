"""Clinical actions inside encounter workspace: diagnosis, treatment, prescription, notes."""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db import transaction

from .models import Encounter
from apps.diagnoses.models import EncounterDiagnosis, DiagnosisCatalog
from apps.treatment.models import TreatmentPlan
from apps.prescriptions.models import Prescription, PrescriptionItem
from apps.clinical.models import ClinicalExamination


def _is_clinician(user):
    return user.is_authenticated and (user.is_doctor or user.role == 'admin')


def _get_open_encounter(pk, user):
    enc = get_object_or_404(Encounter, pk=pk)
    if not _is_clinician(user):
        return None, 'perm'
    if enc.is_locked:
        return None, 'locked'
    return enc, None


@login_required
def update_notes(request, pk):
    enc, err = _get_open_encounter(pk, request.user)
    if err == 'perm':
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    if err == 'locked':
        messages.error(request, _('ویزیت نهایی شده و قابل ویرایش نیست.'))
        return redirect(f'/encounters/{pk}/')
    if request.method == 'POST':
        enc.chief_complaint = request.POST.get('chief_complaint', enc.chief_complaint)
        enc.notes = request.POST.get('notes', enc.notes)
        if enc.status == Encounter.Status.DRAFT:
            enc.status = Encounter.Status.IN_PROGRESS
        enc.save(update_fields=['chief_complaint', 'notes', 'status', 'updated_at'])
        messages.success(request, _('یادداشت ویزیت ذخیره شد.'))
    return redirect(f'/encounters/{pk}/?tab=summary')


@login_required
def add_diagnosis(request, pk):
    enc, err = _get_open_encounter(pk, request.user)
    if err:
        messages.error(request, _('دسترسی مجاز نیست یا ویزیت قفل است.'))
        return redirect(f'/encounters/{pk}/')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        catalog_id = request.POST.get('catalog') or None
        catalog = None
        if catalog_id:
            catalog = DiagnosisCatalog.objects.filter(pk=catalog_id).first()
            if catalog and not title:
                title = catalog.title_fa
        if not title:
            messages.error(request, _('عنوان تشخیص الزامی است.'))
            return redirect(f'/encounters/{pk}/')
        EncounterDiagnosis.objects.create(
            encounter=enc,
            catalog=catalog,
            title=title,
            code=request.POST.get('code', '') or (catalog.code if catalog else ''),
            priority=request.POST.get('priority') or 'primary',
            side=request.POST.get('side') or 'na',
            clinical_notes=request.POST.get('clinical_notes', ''),
        )
        messages.success(request, _('تشخیص ثبت شد.'))
    return redirect(f'/encounters/{pk}/?tab=dx')


@login_required
def add_treatment(request, pk):
    enc, err = _get_open_encounter(pk, request.user)
    if err:
        messages.error(request, _('دسترسی مجاز نیست یا ویزیت قفل است.'))
        return redirect(f'/encounters/{pk}/')
    if request.method == 'POST':
        plan = TreatmentPlan(
            encounter=enc,
            conservative=request.POST.get('conservative', ''),
            physiotherapy=request.POST.get('physiotherapy', ''),
            immobilization=request.POST.get('immobilization', ''),
            weight_bearing=request.POST.get('weight_bearing', ''),
            medication_recommendations=request.POST.get('medication_recommendations', ''),
            surgical_consideration=request.POST.get('surgical_consideration', ''),
            followup_instructions=request.POST.get('followup_instructions', ''),
        )
        if request.POST.get('finalize') == '1':
            plan.status = TreatmentPlan.Status.FINALIZED
            plan.finalized_by = request.user
            plan.finalized_at = timezone.now()
        plan.save()
        messages.success(request, _('طرح درمان ذخیره شد.'))
    return redirect(f'/encounters/{pk}/?tab=tx')


@login_required
def add_prescription(request, pk):
    enc, err = _get_open_encounter(pk, request.user)
    if err:
        messages.error(request, _('دسترسی مجاز نیست یا ویزیت قفل است.'))
        return redirect(f'/encounters/{pk}/')
    if request.method == 'POST':
        with transaction.atomic():
            rx = Prescription.objects.create(
                encounter=enc,
                patient=enc.patient,
                notes=request.POST.get('notes', ''),
                status=Prescription.Status.DRAFT,
            )
            # Multiple items: medication_name_0, dosage_0, ...
            i = 0
            added = 0
            while True:
                name = request.POST.get(f'medication_name_{i}', '').strip()
                if not name and i > 0 and not request.POST.get(f'medication_name_{i+1}'):
                    # also check single-item fallback
                    break
                if not name:
                    if i == 0:
                        # single fields without index
                        name = request.POST.get('medication_name', '').strip()
                        if name:
                            PrescriptionItem.objects.create(
                                prescription=rx,
                                medication_name=name,
                                dosage=request.POST.get('dosage', ''),
                                frequency=request.POST.get('frequency', ''),
                                duration=request.POST.get('duration', ''),
                                route=request.POST.get('route', ''),
                                instructions=request.POST.get('instructions', ''),
                                order=0,
                            )
                            added += 1
                    break
                PrescriptionItem.objects.create(
                    prescription=rx,
                    medication_name=name,
                    dosage=request.POST.get(f'dosage_{i}', ''),
                    frequency=request.POST.get(f'frequency_{i}', ''),
                    duration=request.POST.get(f'duration_{i}', ''),
                    route=request.POST.get(f'route_{i}', ''),
                    instructions=request.POST.get(f'instructions_{i}', ''),
                    order=i,
                )
                added += 1
                i += 1
                if i > 20:
                    break
            if request.POST.get('approve') == '1':
                rx.status = Prescription.Status.APPROVED
                rx.approved_by = request.user
                rx.approved_at = timezone.now()
                rx.save(update_fields=['status', 'approved_by', 'approved_at', 'updated_at'])
            if added:
                messages.success(request, _('نسخه با %(n)s قلم دارو ثبت شد.') % {'n': added})
            else:
                messages.warning(request, _('نسخه بدون قلم دارو ذخیره شد.'))
    return redirect(f'/encounters/{pk}/?tab=rx')


@login_required
def approve_prescription(request, pk, rx_id):
    if not _is_clinician(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    enc = get_object_or_404(Encounter, pk=pk)
    rx = get_object_or_404(Prescription, pk=rx_id, encounter=enc)
    if enc.is_locked:
        messages.error(request, _('ویزیت قفل است.'))
        return redirect(f'/encounters/{pk}/')
    rx.status = Prescription.Status.APPROVED
    rx.approved_by = request.user
    rx.approved_at = timezone.now()
    rx.save(update_fields=['status', 'approved_by', 'approved_at', 'updated_at'])
    messages.success(request, _('نسخه تأیید شد.'))
    return redirect(f'/encounters/{pk}/?tab=rx')
