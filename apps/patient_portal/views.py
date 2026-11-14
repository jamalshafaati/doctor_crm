from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.utils import timezone
from apps.patients.models import Patient
from apps.appointments.models import Appointment
from apps.prescriptions.models import Prescription
from .models import PublishedDocument, AppointmentRequest


def _get_patient_for_user(user):
    """Resolve Patient record linked to this portal user."""
    if hasattr(user, 'patient_record') and user.patient_record:
        return user.patient_record
    # Fallback: match by linked user FK
    return Patient.objects.filter(user=user).first()


@login_required
def portal_dashboard(request):
    if not (request.user.is_patient or request.user.role == 'patient'):
        # Staff can peek if they have a patient context later; for now redirect
        if request.user.is_doctor or request.user.is_receptionist or request.user.role == 'admin':
            messages.info(request, _('پورتال بیمار مخصوص حساب بیمار است.'))
            return redirect('dashboard')
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('accounts:login')

    patient = _get_patient_for_user(request.user)
    if not patient:
        return render(request, 'portal/no_profile.html', {
            'page_title': _('پورتال بیمار'),
        })

    upcoming = Appointment.objects.filter(
        patient=patient,
        scheduled_at__gte=timezone.now(),
        status__in=['scheduled', 'confirmed'],
    ).order_by('scheduled_at')[:5]

    docs = PublishedDocument.objects.filter(patient=patient, is_published=True)[:10]
    requests = AppointmentRequest.objects.filter(patient=patient).order_by('-created_at')[:5]

    return render(request, 'portal/dashboard.html', {
        'patient': patient,
        'upcoming': upcoming,
        'docs': docs,
        'requests': requests,
        'page_title': _('پورتال من'),
    })


@login_required
def portal_documents(request):
    patient = _get_patient_for_user(request.user)
    if not patient:
        messages.error(request, _('پروفایل بیمار یافت نشد.'))
        return redirect('portal:dashboard')
    docs = PublishedDocument.objects.filter(patient=patient, is_published=True)
    return render(request, 'portal/documents.html', {
        'patient': patient, 'docs': docs, 'page_title': _('اسناد پزشکی'),
    })


@login_required
def portal_document_detail(request, pk):
    patient = _get_patient_for_user(request.user)
    doc = get_object_or_404(PublishedDocument, pk=pk, patient=patient, is_published=True)
    return render(request, 'portal/document_detail.html', {
        'patient': patient, 'doc': doc, 'page_title': doc.title,
    })


@login_required
def portal_appointments(request):
    patient = _get_patient_for_user(request.user)
    if not patient:
        messages.error(request, _('پروفایل بیمار یافت نشد.'))
        return redirect('portal:dashboard')
    appointments = Appointment.objects.filter(patient=patient).order_by('-scheduled_at')[:30]
    requests = AppointmentRequest.objects.filter(patient=patient).order_by('-created_at')[:10]
    return render(request, 'portal/appointments.html', {
        'patient': patient, 'appointments': appointments, 'requests': requests,
        'page_title': _('نوبت‌های من'),
    })


@login_required
def portal_request_appointment(request):
    patient = _get_patient_for_user(request.user)
    if not patient:
        messages.error(request, _('پروفایل بیمار یافت نشد.'))
        return redirect('portal:dashboard')
    if request.method == 'POST':
        preferred_date = request.POST.get('preferred_date')
        preferred_time = request.POST.get('preferred_time') or None
        reason = request.POST.get('reason', '')
        if preferred_date:
            AppointmentRequest.objects.create(
                patient=patient,
                preferred_date=preferred_date,
                preferred_time=preferred_time or None,
                reason=reason,
            )
            messages.success(request, _('درخواست نوبت ثبت شد. پذیرش با شما تماس خواهد گرفت.'))
            return redirect('portal:appointments')
        messages.error(request, _('تاریخ ترجیحی الزامی است.'))
    return render(request, 'portal/request_appointment.html', {
        'patient': patient, 'page_title': _('درخواست نوبت'),
    })


@login_required
def portal_prescriptions(request):
    patient = _get_patient_for_user(request.user)
    if not patient:
        messages.error(request, _('پروفایل بیمار یافت نشد.'))
        return redirect('portal:dashboard')
    # Only show prescriptions that were published OR approved
    # For MVP: show approved prescriptions; publication gate via PublishedDocument for summaries
    rxs = Prescription.objects.filter(
        patient=patient, status='approved'
    ).prefetch_related('items').order_by('-created_at')[:20]
    return render(request, 'portal/prescriptions.html', {
        'patient': patient, 'prescriptions': rxs, 'page_title': _('نسخه‌های من'),
    })


# --- Doctor side: publish document ---
@login_required
def publish_document(request, patient_id):
    if not (request.user.is_doctor or request.user.role == 'admin'):
        messages.error(request, _('فقط پزشک می‌تواند سند منتشر کند.'))
        return redirect('dashboard')
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        doc_type = request.POST.get('doc_type', 'other')
        content = request.POST.get('content', '')
        if title:
            PublishedDocument.objects.create(
                patient=patient,
                title=title,
                doc_type=doc_type,
                content=content,
                published_by=request.user,
                is_published=True,
            )
            messages.success(request, _('سند برای بیمار منتشر شد.'))
            return redirect('patients:detail', pk=patient.pk)
        messages.error(request, _('عنوان الزامی است.'))
    return render(request, 'portal/publish_form.html', {
        'patient': patient,
        'doc_types': PublishedDocument.DocType.choices,
        'page_title': _('انتشار سند برای بیمار'),
    })
