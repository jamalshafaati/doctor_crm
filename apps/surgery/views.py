from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from .models import Surgery, Implant
from .forms import SurgeryForm, ImplantForm


def _is_clinician(user):
    return user.is_authenticated and (user.is_doctor or user.role == 'admin')


@login_required
def surgery_list(request):
    if not (request.user.is_doctor or request.user.is_receptionist or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    qs = Surgery.objects.select_related('patient', 'surgeon').order_by('-surgery_date')
    status = request.GET.get('status', '')
    if status:
        qs = qs.filter(status=status)
    return render(request, 'surgery/list.html', {
        'surgeries': qs[:50],
        'status': status,
        'statuses': Surgery.Status.choices,
        'page_title': _('جراحی‌ها'),
    })


@login_required
def surgery_create(request):
    if not _is_clinician(request.user):
        messages.error(request, _('فقط پزشک می‌تواند رکورد جراحی ثبت کند.'))
        return redirect('dashboard')
    if request.method == 'POST':
        form = SurgeryForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            messages.success(request, _('رکورد جراحی ثبت شد.'))
            return redirect('surgery:detail', pk=obj.pk)
    else:
        initial = {}
        if request.user.is_doctor:
            initial['surgeon'] = request.user.pk
        patient_id = request.GET.get('patient')
        if patient_id:
            initial['patient'] = patient_id
        form = SurgeryForm(initial=initial)
    return render(request, 'surgery/form.html', {
        'form': form, 'page_title': _('ثبت جراحی جدید'), 'is_create': True,
    })


@login_required
def surgery_detail(request, pk):
    if not (request.user.is_doctor or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    surgery = get_object_or_404(
        Surgery.objects.select_related('patient', 'surgeon').prefetch_related('implants', 'followups'),
        pk=pk
    )
    implant_form = ImplantForm()
    return render(request, 'surgery/detail.html', {
        'surgery': surgery,
        'implant_form': implant_form,
        'page_title': surgery.procedure,
    })


@login_required
def surgery_edit(request, pk):
    if not _is_clinician(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    surgery = get_object_or_404(Surgery, pk=pk)
    if request.method == 'POST':
        form = SurgeryForm(request.POST, instance=surgery)
        if form.is_valid():
            form.save()
            messages.success(request, _('رکورد جراحی به‌روزرسانی شد.'))
            return redirect('surgery:detail', pk=surgery.pk)
    else:
        form = SurgeryForm(instance=surgery)
    return render(request, 'surgery/form.html', {
        'form': form, 'surgery': surgery, 'page_title': _('ویرایش جراحی'), 'is_create': False,
    })


@login_required
def implant_add(request, surgery_id):
    if not _is_clinician(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    surgery = get_object_or_404(Surgery, pk=surgery_id)
    if request.method == 'POST':
        form = ImplantForm(request.POST)
        if form.is_valid():
            implant = form.save(commit=False)
            implant.surgery = surgery
            implant.save()
            messages.success(request, _('ایمپلنت اضافه شد.'))
        else:
            messages.error(request, _('خطا در ثبت ایمپلنت.'))
    return redirect('surgery:detail', pk=surgery.pk)
