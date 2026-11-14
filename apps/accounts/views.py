from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import timedelta


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next') or 'dashboard'
                return redirect(next_url)
            messages.error(request, _('حساب کاربری شما غیرفعال است.'))
        else:
            messages.error(request, _('نام کاربری یا رمز عبور اشتباه است.'))
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, _('با موفقیت خارج شدید.'))
    return redirect('accounts:login')


@login_required
def dashboard(request):
    from apps.patients.models import Patient
    from apps.appointments.models import Appointment
    from apps.encounters.models import Encounter
    from apps.followups.models import FollowUp
    from apps.surgery.models import Surgery
    from apps.notifications.models import Notification

    user = request.user
    today = timezone.localdate()
    week_ago = today - timedelta(days=7)

    unread = Notification.objects.filter(recipient=user, is_read=False).count()

    if user.is_doctor or user.role == 'admin':
        appts_today = Appointment.objects.filter(scheduled_at__date=today).select_related('patient', 'doctor').order_by('scheduled_at')
        open_encounters = Encounter.objects.exclude(
            status__in=['finalized', 'amended']
        ).select_related('patient', 'doctor').order_by('-started_at')[:10]
        followups_today = FollowUp.objects.filter(
            scheduled_date=today
        ).select_related('patient', 'doctor').order_by('scheduled_date')
        recent_patients = Patient.objects.filter(is_active=True).order_by('-registered_at')[:8]
        surgeries_upcoming = Surgery.objects.filter(
            surgery_date__gte=today, status='planned'
        ).select_related('patient').order_by('surgery_date')[:5]

        context = {
            'page_title': _('داشبورد پزشک'),
            'unread_notifications': unread,
            'metrics': {
                'patients_total': Patient.objects.filter(is_active=True).count(),
                'appointments_today': appts_today.count(),
                'open_encounters': Encounter.objects.exclude(status__in=['finalized', 'amended']).count(),
                'followups_today': followups_today.count(),
                'new_patients_week': Patient.objects.filter(registered_at__date__gte=week_ago).count(),
                'surgeries_planned': Surgery.objects.filter(status='planned', surgery_date__gte=today).count(),
            },
            'appts_today': appts_today[:15],
            'open_encounters': open_encounters,
            'followups_today': followups_today[:10],
            'recent_patients': recent_patients,
            'surgeries_upcoming': surgeries_upcoming,
        }
        return render(request, 'dashboard/doctor.html', context)

    if user.is_receptionist:
        appts_today = Appointment.objects.filter(
            scheduled_at__date=today
        ).select_related('patient', 'doctor').order_by('scheduled_at')
        waiting = appts_today.filter(status='checked_in')
        context = {
            'page_title': _('داشبورد پذیرش'),
            'unread_notifications': unread,
            'metrics': {
                'appointments_today': appts_today.count(),
                'waiting_patients': waiting.count(),
                'new_registrations': Patient.objects.filter(registered_at__date=today).count(),
                'cancelled_today': appts_today.filter(status='cancelled').count(),
                'confirmed': appts_today.filter(status__in=['scheduled', 'confirmed']).count(),
            },
            'appts_today': appts_today,
            'waiting': waiting,
            'recent_patients': Patient.objects.order_by('-registered_at')[:8],
        }
        return render(request, 'dashboard/receptionist.html', context)

    # patient role → portal
    if user.is_patient or user.role == 'patient':
        return redirect('portal:dashboard')

    return render(request, 'dashboard/index.html', {'page_title': _('داشبورد')})
