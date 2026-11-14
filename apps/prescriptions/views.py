from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from .models import Prescription


@login_required
def prescription_list(request):
    if not (request.user.is_doctor or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    rxs = Prescription.objects.select_related('patient').prefetch_related('items').order_by('-created_at')[:50]
    return render(request, 'prescriptions/list.html', {
        'prescriptions': rxs,
        'page_title': _('نسخه‌ها'),
    })
