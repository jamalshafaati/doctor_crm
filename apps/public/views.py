from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from apps.accounts.models import ClinicSettings, User
from apps.core.dates import parse_jalali_date
from apps.patient_portal.models import AppointmentRequest
from apps.patients.models import Patient


def home(request):
    clinic = ClinicSettings.get_solo()
    doctors = User.objects.filter(role='doctor', is_active=True).select_related('doctor_profile')
    return render(request, 'public/home.html', {
        'clinic': clinic,
        'doctors': doctors,
        'page_title': clinic.name_fa or _('کلینیک تخصصی پا و مچ پا'),
    })


def about(request):
    clinic = ClinicSettings.get_solo()
    doctors = User.objects.filter(role='doctor', is_active=True).select_related('doctor_profile')
    return render(request, 'public/about.html', {
        'clinic': clinic, 'doctors': doctors, 'page_title': _('درباره ما'),
    })


def services(request):
    clinic = ClinicSettings.get_solo()
    return render(request, 'public/services.html', {
        'clinic': clinic, 'page_title': _('خدمات تخصصی'),
    })


@require_http_methods(['GET', 'POST'])
def book(request):
    clinic = ClinicSettings.get_solo()
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        preferred = request.POST.get('preferred_date', '')
        reason = request.POST.get('reason', '')
        if not name or not phone:
            messages.error(request, _('نام و تلفن الزامی است.'))
        else:
            # Match or create minimal patient shell for request tracking
            patient = Patient.objects.filter(phone=phone).first()
            if not patient:
                parts = name.split(None, 1)
                patient = Patient.objects.create(
                    first_name=parts[0],
                    last_name=parts[1] if len(parts) > 1 else '—',
                    phone=phone,
                    notes=f'ثبت از وب‌سایت عمومی',
                )
            d = parse_jalali_date(preferred)
            from django.utils import timezone
            AppointmentRequest.objects.create(
                patient=patient,
                preferred_date=d or timezone.localdate(),
                reason=f"{reason}\n(درخواست وب‌سایت — {name} — {phone})",
            )
            # Notify reception users
            try:
                from apps.notifications.services import notify_user
                for u in User.objects.filter(role__in=['receptionist', 'admin'], is_active=True):
                    notify_user(u, f'درخواست نوبت جدید: {name}', f'{phone} — {reason[:80]}', category='appointment', link='/appointments/')
            except Exception:
                pass
            messages.success(request, _('درخواست نوبت ثبت شد. پذیرش به‌زودی تماس می‌گیرد.'))
            return redirect('public:book')
    return render(request, 'public/book.html', {
        'clinic': clinic, 'page_title': _('رزرو نوبت آنلاین'),
    })


def contact(request):
    clinic = ClinicSettings.get_solo()
    return render(request, 'public/contact.html', {
        'clinic': clinic, 'page_title': _('تماس با ما'),
    })
