from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db import transaction
from .models import Encounter
from apps.patients.models import Patient
from apps.appointments.models import Appointment
from apps.accounts.models import User
from apps.diagnoses.models import DiagnosisCatalog


def _is_clinician(user):
    return user.is_authenticated and (user.is_doctor or user.role == 'admin')


@login_required
def encounter_list(request):
    if not (request.user.is_doctor or request.user.is_receptionist or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')

    status = request.GET.get('status', '')
    qs = Encounter.objects.select_related('patient', 'doctor').order_by('-started_at')
    if status:
        qs = qs.filter(status=status)
    else:
        qs = qs.exclude(status=Encounter.Status.FINALIZED)[:50]

    return render(request, 'encounters/list.html', {
        'encounters': qs,
        'status': status,
        'statuses': Encounter.Status.choices,
        'page_title': _('ویزیت‌ها'),
    })


@login_required
def encounter_create(request):
    """Create walk-in or from appointment."""
    if not _is_clinician(request.user) and not request.user.is_receptionist:
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')

    patient_id = request.GET.get('patient') or request.POST.get('patient')
    appointment_id = request.GET.get('appointment') or request.POST.get('appointment')

    if request.method == 'POST':
        patient = get_object_or_404(Patient, pk=patient_id)
        doctor_id = request.POST.get('doctor') or (
            request.user.pk if request.user.is_doctor else None
        )
        if not doctor_id:
            messages.error(request, _('پزشک را انتخاب کنید.'))
            return redirect('encounters:list')

        doctor = get_object_or_404(User, pk=doctor_id, role__in=['doctor', 'admin'])
        appointment = None
        if appointment_id:
            appointment = get_object_or_404(Appointment, pk=appointment_id)

        with transaction.atomic():
            enc = Encounter.objects.create(
                patient=patient,
                doctor=doctor,
                appointment=appointment,
                status=Encounter.Status.IN_PROGRESS,
                chief_complaint=request.POST.get('chief_complaint', ''),
                started_at=timezone.now(),
            )
            if appointment and appointment.status in [
                Appointment.Status.SCHEDULED, Appointment.Status.CONFIRMED, Appointment.Status.CHECKED_IN
            ]:
                appointment.status = Appointment.Status.COMPLETED
                appointment.save(update_fields=['status', 'updated_at'])

        messages.success(request, _('ویزیت ایجاد شد.'))
        return redirect('encounters:workspace', pk=enc.pk)

    patients = Patient.objects.filter(is_active=True).order_by('last_name')[:100]
    doctors = User.objects.filter(role='doctor', is_active=True)
    return render(request, 'encounters/create.html', {
        'patients': patients,
        'doctors': doctors,
        'patient_id': patient_id,
        'page_title': _('شروع ویزیت جدید'),
    })


@login_required
def encounter_workspace(request, pk):
    """Main clinical workspace for a visit."""
    if not _is_clinician(request.user):
        messages.error(request, _('فقط پزشک به فضای کاری بالینی دسترسی دارد.'))
        return redirect('dashboard')

    enc = get_object_or_404(
        Encounter.objects.select_related('patient', 'doctor', 'appointment'),
        pk=pk
    )
    patient = enc.patient
    allergies = patient.allergies.filter(is_active=True)
    alerts = patient.alerts.filter(is_active=True)
    history = getattr(patient, 'medical_history', None)

    clinical_exams = enc.clinical_exams.all()
    trauma_exams = enc.trauma_exams.all()
    sports_exams = enc.sports_exams.all()
    achilles_exams = enc.achilles_exams.all()
    flatfoot_exams = enc.flatfoot_exams.all()
    deformity_exams = enc.deformity_exams.all()
    arthritis_exams = enc.arthritis_exams.all()
    anatomy = enc.anatomy_findings.all()
    diagnoses = enc.diagnoses.all()
    imaging = enc.imaging_studies.all()
    treatments = enc.treatment_plans.all()
    prescriptions = enc.prescriptions.prefetch_related('items').all()

    return render(request, 'encounters/workspace.html', {
        'encounter': enc,
        'patient': patient,
        'allergies': allergies,
        'alerts': alerts,
        'history': history,
        'clinical_exams': clinical_exams,
        'trauma_exams': trauma_exams,
        'sports_exams': sports_exams,
        'achilles_exams': achilles_exams,
        'flatfoot_exams': flatfoot_exams,
        'deformity_exams': deformity_exams,
        'arthritis_exams': arthritis_exams,
        'anatomy': anatomy,
        'diagnoses': diagnoses,
        'imaging': imaging,
        'treatments': treatments,
        'prescriptions': prescriptions,
        'page_title': _('فضای کاری ویزیت'),
        'diagnosis_catalog': DiagnosisCatalog.objects.filter(is_active=True).order_by('title_fa'),
        'tab': request.GET.get('tab', 'summary'),
    })


@login_required
def encounter_finalize(request, pk):
    if not _is_clinician(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')

    enc = get_object_or_404(Encounter, pk=pk)
    if request.method == 'POST':
        try:
            enc.finalize(request.user)
            messages.success(request, _('ویزیت نهایی شد.'))
        except ValueError as e:
            messages.error(request, str(e))
    return redirect('encounters:workspace', pk=pk)


@login_required
def encounter_report(request, pk):
    """Full clinical report for a visit — read-focused, link to workspace for edit."""
    if not (request.user.is_doctor or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    enc = get_object_or_404(
        Encounter.objects.select_related('patient', 'doctor'),
        pk=pk
    )
    patient = enc.patient
    return render(request, 'encounters/report.html', {
        'encounter': enc,
        'patient': patient,
        'allergies': patient.allergies.filter(is_active=True),
        'alerts': patient.alerts.filter(is_active=True),
        'history': getattr(patient, 'medical_history', None),
        'clinical_exams': enc.clinical_exams.all(),
        'trauma_exams': enc.trauma_exams.all(),
        'achilles_exams': enc.achilles_exams.all(),
        'sports_exams': enc.sports_exams.all(),
        'flatfoot_exams': enc.flatfoot_exams.all(),
        'deformity_exams': enc.deformity_exams.all(),
        'arthritis_exams': enc.arthritis_exams.all(),
        'anatomy': enc.anatomy_findings.all(),
        'diagnoses': enc.diagnoses.all(),
        'treatments': enc.treatment_plans.all(),
        'prescriptions': enc.prescriptions.prefetch_related('items').all(),
        'page_title': _('گزارش ویزیت'),
    })
