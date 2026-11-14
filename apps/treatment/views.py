from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from .models import TreatmentPlan


@login_required
def treatment_list(request):
    if not (request.user.is_doctor or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    plans = TreatmentPlan.objects.select_related('encounter', 'encounter__patient').order_by('-created_at')[:50]
    return render(request, 'treatment/list.html', {
        'plans': plans,
        'page_title': _('طرح‌های درمان'),
    })
