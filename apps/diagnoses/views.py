from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from .models import DiagnosisCatalog, EncounterDiagnosis


@login_required
def diagnosis_list(request):
    if not (request.user.is_doctor or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    catalog = DiagnosisCatalog.objects.filter(is_active=True)
    recent = EncounterDiagnosis.objects.select_related('encounter', 'encounter__patient').order_by('-created_at')[:30]
    return render(request, 'diagnoses/list.html', {
        'catalog': catalog,
        'recent': recent,
        'page_title': _('تشخیص‌ها'),
    })
