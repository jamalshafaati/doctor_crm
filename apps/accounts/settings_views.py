from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from .models import ClinicSettings


@login_required
def clinic_settings(request):
    if not (request.user.is_doctor or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    settings_obj = ClinicSettings.get_solo()
    if request.method == 'POST':
        settings_obj.name_fa = request.POST.get('name_fa', settings_obj.name_fa)
        settings_obj.name_en = request.POST.get('name_en', settings_obj.name_en)
        settings_obj.address = request.POST.get('address', '')
        settings_obj.phone = request.POST.get('phone', '')
        settings_obj.email = request.POST.get('email', '')
        settings_obj.working_hours = request.POST.get('working_hours', '')
        settings_obj.save()
        messages.success(request, _('تنظیمات ذخیره شد.'))
        return redirect('accounts:settings')
    return render(request, 'accounts/settings.html', {
        'clinic': settings_obj,
        'page_title': _('تنظیمات کلینیک'),
    })
