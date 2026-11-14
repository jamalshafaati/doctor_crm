from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
from django.conf import settings
import os

from .forms import PatientForm, AllergyForm, ClinicalAlertForm, MedicalHistoryForm
from .models import Patient
from .services import create_patient, update_patient, search_patients
from apps.medical_history.models import Allergy, ClinicalAlert, MedicalHistory
from apps.documents.models import PatientDocument
from apps.appointments.models import Appointment
from apps.encounters.models import Encounter
from apps.surgery.models import Surgery
from apps.followups.models import FollowUp
from apps.prescriptions.models import Prescription
from apps.patient_portal.models import PublishedDocument


def _can_manage_patients(user):
    return user.is_authenticated and (
        user.is_doctor or user.is_receptionist or user.role == 'admin'
    )


@login_required
def patient_list(request):
    if not _can_manage_patients(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    q = request.GET.get('q', '').strip()
    gender = request.GET.get('gender', '')
    has_surgery = request.GET.get('has_surgery', '')
    has_allergy = request.GET.get('has_allergy', '')
    patients = search_patients(
        query=q,
        gender=gender or None,
        has_surgery=True if has_surgery == '1' else (False if has_surgery == '0' else None),
        has_allergy=True if has_allergy == '1' else None,
    )
    paginator = Paginator(patients, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'patients/list.html', {
        'page_obj': page, 'q': q, 'gender': gender,
        'has_surgery': has_surgery, 'has_allergy': has_allergy,
        'page_title': _('لیست بیماران'),
    })


@login_required
def patient_create(request):
    if not _can_manage_patients(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = create_patient(**{k: v for k, v in form.cleaned_data.items()})
            messages.success(request, _('بیمار با موفقیت ثبت شد. شماره پرونده: %(num)s') % {
                'num': patient.patient_number
            })
            return redirect('patients:detail', pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, 'patients/form.html', {
        'form': form, 'page_title': _('ثبت بیمار جدید'), 'is_create': True,
    })


@login_required
def patient_detail(request, pk):
    if not _can_manage_patients(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')

    patient = get_object_or_404(Patient, pk=pk)
    tab = request.GET.get('tab', 'overview')

    context = {
        'patient': patient,
        'tab': tab,
        'page_title': patient.full_name,
        'allergy_form': AllergyForm(),
        'alert_form': ClinicalAlertForm(),
        'allergies': patient.allergies.all().order_by('-is_active', '-severity'),
        'alerts': patient.alerts.filter(is_active=True),
        'history': getattr(patient, 'medical_history', None),
        'appointments': patient.appointments.select_related('doctor').order_by('-scheduled_at')[:15],
        'encounters': patient.encounters.select_related('doctor').order_by('-started_at')[:15],
        'surgeries': patient.surgeries.select_related('surgeon').order_by('-surgery_date')[:10],
        'followups': patient.followups.select_related('doctor').order_by('-scheduled_date')[:10],
        'prescriptions': patient.prescriptions.prefetch_related('items').order_by('-created_at')[:10],
        'documents': patient.documents.select_related('uploaded_by').order_by('-created_at')[:30],
        'published_docs': patient.published_documents.filter(is_published=True).order_by('-published_at')[:15],
        'doc_categories': PatientDocument.Category.choices,
    }
    # Medical history form
    history = context['history']
    if history:
        context['history_form'] = MedicalHistoryForm(instance=history)
    else:
        context['history_form'] = MedicalHistoryForm()

    return render(request, 'patients/detail.html', context)


@login_required
def patient_edit(request, pk):
    if not _can_manage_patients(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            update_patient(patient, **form.cleaned_data)
            messages.success(request, _('اطلاعات بیمار به‌روزرسانی شد.'))
            return redirect('patients:detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/form.html', {
        'form': form, 'patient': patient, 'page_title': _('ویرایش بیمار'), 'is_create': False,
    })


@login_required
def allergy_add(request, pk):
    if not _can_manage_patients(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = AllergyForm(request.POST)
        if form.is_valid():
            allergy = form.save(commit=False)
            allergy.patient = patient
            allergy.save()
            messages.success(request, _('آلرژی ثبت شد.'))
        else:
            messages.error(request, _('خطا در ثبت آلرژی.'))
    return redirect(f"{reverse_detail(pk)}?tab=clinical")


@login_required
def allergy_delete(request, pk, allergy_id):
    if not _can_manage_patients(request.user):
        return redirect('dashboard')
    allergy = get_object_or_404(Allergy, pk=allergy_id, patient_id=pk)
    if request.method == 'POST':
        allergy.is_active = False
        allergy.save(update_fields=['is_active'])
        messages.success(request, _('آلرژی غیرفعال شد.'))
    return redirect(f"/patients/{pk}/?tab=clinical")


@login_required
def alert_add(request, pk):
    if not (request.user.is_doctor or request.user.role == 'admin'):
        messages.error(request, _('فقط پزشک می‌تواند هشدار بالینی ثبت کند.'))
        return redirect('patients:detail', pk=pk)
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = ClinicalAlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.patient = patient
            alert.created_by = request.user
            alert.save()
            messages.success(request, _('هشدار بالینی ثبت شد.'))
    return redirect(f"/patients/{pk}/?tab=clinical")


@login_required
def history_save(request, pk):
    if not (request.user.is_doctor or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('patients:detail', pk=pk)
    patient = get_object_or_404(Patient, pk=pk)
    history, _ = MedicalHistory.objects.get_or_create(patient=patient)
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST, instance=history)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user
            obj.save()
            messages.success(request, _('سابقه پزشکی ذخیره شد.'))
    return redirect(f"/patients/{pk}/?tab=history")


@login_required
def document_upload(request, pk):
    if not _can_manage_patients(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST' and request.FILES.get('file'):
        f = request.FILES['file']
        # Basic validation
        max_size = 15 * 1024 * 1024  # 15MB
        if f.size > max_size:
            messages.error(request, _('حجم فایل بیش از ۱۵ مگابایت است.'))
            return redirect(f"/patients/{pk}/?tab=documents")
        allowed = {
            '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.webp',
            '.doc', '.docx', '.xls', '.xlsx', '.txt',
        }
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in allowed:
            messages.error(request, _('نوع فایل مجاز نیست.'))
            return redirect(f"/patients/{pk}/?tab=documents")

        doc = PatientDocument(
            patient=patient,
            title=request.POST.get('title') or f.name,
            category=request.POST.get('category') or 'other',
            description=request.POST.get('description', ''),
            file=f,
            original_filename=f.name,
            content_type=getattr(f, 'content_type', '') or '',
            file_size=f.size,
            uploaded_by=request.user,
        )
        doc.save()
        messages.success(request, _('فایل با موفقیت آپلود شد.'))
    else:
        messages.error(request, _('فایلی انتخاب نشده است.'))
    return redirect(f"/patients/{pk}/?tab=documents")


@login_required
def document_download(request, pk, doc_id):
    if not _can_manage_patients(request.user):
        raise Http404
    doc = get_object_or_404(PatientDocument, pk=doc_id, patient_id=pk)
    if not doc.file:
        raise Http404
    try:
        return FileResponse(
            doc.file.open('rb'),
            as_attachment=True,
            filename=doc.original_filename or doc.title,
        )
    except FileNotFoundError:
        raise Http404


def reverse_detail(pk):
    return f"/patients/{pk}/"
