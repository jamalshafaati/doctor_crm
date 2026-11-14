from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from .models import ImagingStudy


@login_required
def imaging_list(request):
    if not (request.user.is_doctor or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    studies = ImagingStudy.objects.select_related('patient').order_by('-created_at')[:50]
    return render(request, 'imaging/list.html', {
        'studies': studies,
        'page_title': _('تصویربرداری'),
    })
