from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from apps.core.dates import parse_jalali_date, to_jalali
from apps.patients.models import Patient
from apps.appointments.models import Appointment
from apps.encounters.models import Encounter
from apps.surgery.models import Surgery
from apps.followups.models import FollowUp
from apps.prescriptions.models import Prescription


@login_required
def reports_dashboard(request):
    if not (request.user.is_doctor or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')

    today = timezone.localdate()
    # Date range from Jalali or Gregorian inputs
    from_s = request.GET.get('from', '')
    to_s = request.GET.get('to', '')
    date_from = parse_jalali_date(from_s) if from_s else (today - timedelta(days=30))
    date_to = parse_jalali_date(to_s) if to_s else today
    if date_from and date_to and date_from > date_to:
        date_from, date_to = date_to, date_from

    appt_qs = Appointment.objects.filter(scheduled_at__date__gte=date_from, scheduled_at__date__lte=date_to)
    enc_qs = Encounter.objects.filter(started_at__date__gte=date_from, started_at__date__lte=date_to)
    surgery_qs = Surgery.objects.filter(surgery_date__gte=date_from, surgery_date__lte=date_to)
    fu_qs = FollowUp.objects.filter(scheduled_date__gte=date_from, scheduled_date__lte=date_to)
    new_patients = Patient.objects.filter(registered_at__date__gte=date_from, registered_at__date__lte=date_to).count()

    appt_by_status = list(appt_qs.values('status').annotate(c=Count('id')).order_by('status'))
    enc_by_status = list(enc_qs.values('status').annotate(c=Count('id')).order_by('status'))
    surgery_by_status = list(surgery_qs.values('status').annotate(c=Count('id')))

    # Daily series
    daily = []
    d = date_from
    while d <= date_to and len(daily) < 62:
        daily.append({
            'date': d,
            'jalali': to_jalali(d),
            'appts': Appointment.objects.filter(scheduled_at__date=d).count(),
            'encounters': Encounter.objects.filter(started_at__date=d).count(),
        })
        d += timedelta(days=1)

    return render(request, 'reports/dashboard.html', {
        'page_title': _('آمار و گزارش'),
        'date_from': date_from,
        'date_to': date_to,
        'date_from_j': to_jalali(date_from),
        'date_to_j': to_jalali(date_to),
        'total_patients': Patient.objects.filter(is_active=True).count(),
        'new_patients': new_patients,
        'appt_count': appt_qs.count(),
        'enc_count': enc_qs.count(),
        'enc_finalized': enc_qs.filter(status='finalized').count(),
        'surgery_count': surgery_qs.count(),
        'followup_count': fu_qs.count(),
        'followup_done': fu_qs.filter(status='completed').count(),
        'rx_count': Prescription.objects.filter(created_at__date__gte=date_from, created_at__date__lte=date_to).count(),
        'appt_by_status': appt_by_status,
        'enc_by_status': enc_by_status,
        'surgery_by_status': surgery_by_status,
        'daily': daily,
        'open_encounters': Encounter.objects.exclude(status__in=['finalized', 'amended']).count(),
    })
