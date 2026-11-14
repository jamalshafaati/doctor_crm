from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from .forms import AppointmentForm
from .models import Appointment
from .services import create_appointment, check_in_appointment, cancel_appointment
from apps.patients.models import Patient
from apps.accounts.models import User


def _can_manage_appointments(user):
    return user.is_authenticated and (
        user.is_doctor or user.is_receptionist or user.role == 'admin'
    )


@login_required
def appointment_list(request):
    if not _can_manage_appointments(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')

    status = request.GET.get('status', '')
    date = request.GET.get('date', '')
    qs = Appointment.objects.select_related('patient', 'doctor').order_by('scheduled_at')

    if status:
        qs = qs.filter(status=status)
    if date:
        qs = qs.filter(scheduled_at__date=date)
    else:
        # Default: today and future
        qs = qs.filter(scheduled_at__date__gte=timezone.localdate())

    paginator = Paginator(qs, 25)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'appointments/list.html', {
        'page_obj': page,
        'status': status,
        'date': date,
        'statuses': Appointment.Status.choices,
        'page_title': _('نوبت‌ها'),
    })


@login_required
def appointment_create(request):
    if not _can_manage_appointments(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')

    initial = {}
    patient_id = request.GET.get('patient')
    if patient_id:
        initial['patient'] = patient_id

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appt = create_appointment(
                    patient=form.cleaned_data['patient'],
                    doctor=form.cleaned_data['doctor'],
                    scheduled_at=form.cleaned_data['scheduled_at'],
                    duration_minutes=form.cleaned_data.get('duration_minutes') or 30,
                    reason=form.cleaned_data.get('reason', ''),
                    notes=form.cleaned_data.get('notes', ''),
                    created_by=request.user,
                )
                messages.success(request, _('نوبت با موفقیت ثبت شد.'))
                return redirect('appointments:list')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = AppointmentForm(initial=initial)

    return render(request, 'appointments/form.html', {
        'form': form,
        'page_title': _('رزرو نوبت جدید'),
        'is_create': True,
    })


@login_required
def appointment_check_in(request, pk):
    if not _can_manage_appointments(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')

    appt = get_object_or_404(Appointment, pk=pk)
    try:
        check_in_appointment(appt)
        messages.success(request, _('چک‌این بیمار انجام شد: %(name)s') % {'name': appt.patient.full_name})
    except ValidationError as e:
        messages.error(request, str(e))
    return redirect(request.META.get('HTTP_REFERER', 'appointments:list'))


@login_required
def appointment_cancel(request, pk):
    if not _can_manage_appointments(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')

    appt = get_object_or_404(Appointment, pk=pk)
    try:
        cancel_appointment(appt)
        messages.success(request, _('نوبت لغو شد.'))
    except ValidationError as e:
        messages.error(request, str(e))
    return redirect('appointments:list')


@login_required
def appointment_calendar(request):
    """Day calendar: show appointments for a Jalali/Gregorian date (default today)."""
    from django.utils import timezone
    from apps.core.dates import parse_jalali_date, to_jalali
    from datetime import timedelta

    if not (request.user.is_doctor or request.user.is_receptionist or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')

    day_s = request.GET.get('day', '')
    day = parse_jalali_date(day_s) if day_s else timezone.localdate()
    if not day:
        day = timezone.localdate()
    prev_day = day - timedelta(days=1)
    next_day = day + timedelta(days=1)
    appts = Appointment.objects.filter(
        scheduled_at__date=day
    ).select_related('patient', 'doctor').order_by('scheduled_at')

    return render(request, 'appointments/calendar.html', {
        'day': day,
        'day_j': to_jalali(day),
        'prev_j': to_jalali(prev_day),
        'next_j': to_jalali(next_day),
        'appointments': appts,
        'page_title': _('تقویم نوبت‌ها'),
    })
