from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from .models import MedicalHistory, Allergy


@login_required
def history_list(request):
    if not (request.user.is_doctor or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    qs = MedicalHistory.objects.select_related('patient').order_by('-updated_at')[:100]
    allergies = Allergy.objects.filter(is_active=True).select_related('patient').order_by('-severity')[:50]
    return render(request, 'medical_history/list.html', {
        'histories': qs,
        'allergies': allergies,
        'page_title': _('سوابق پزشکی'),
    })
