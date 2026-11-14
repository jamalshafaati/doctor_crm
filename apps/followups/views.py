from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.utils import timezone
from .models import FollowUp
from .forms import FollowUpForm


def _is_clinician(user):
    return user.is_authenticated and (user.is_doctor or user.role == 'admin')


@login_required
def followup_list(request):
    if not (request.user.is_doctor or request.user.is_receptionist or request.user.role == 'admin'):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    qs = FollowUp.objects.select_related('patient', 'doctor', 'surgery').order_by('-scheduled_date')
    status = request.GET.get('status', '')
    if status:
        qs = qs.filter(status=status)
    return render(request, 'followups/list.html', {
        'followups': qs[:50],
        'status': status,
        'statuses': FollowUp.Status.choices,
        'page_title': _('پیگیری‌ها'),
    })


@login_required
def followup_create(request):
    if not _is_clinician(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    if request.method == 'POST':
        form = FollowUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('پیگیری ثبت شد.'))
            return redirect('followups:list')
    else:
        initial = {}
        if request.user.is_doctor:
            initial['doctor'] = request.user.pk
        if request.GET.get('patient'):
            initial['patient'] = request.GET['patient']
        if request.GET.get('surgery'):
            initial['surgery'] = request.GET['surgery']
        form = FollowUpForm(initial=initial)
    return render(request, 'followups/form.html', {
        'form': form, 'page_title': _('ثبت پیگیری جدید'), 'is_create': True,
    })


@login_required
def followup_detail(request, pk):
    if not _is_clinician(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    fu = get_object_or_404(
        FollowUp.objects.select_related('patient', 'doctor', 'surgery'),
        pk=pk
    )
    return render(request, 'followups/detail.html', {
        'followup': fu, 'page_title': _('پیگیری'),
    })


@login_required
def followup_edit(request, pk):
    if not _is_clinician(request.user):
        messages.error(request, _('دسترسی مجاز نیست.'))
        return redirect('dashboard')
    fu = get_object_or_404(FollowUp, pk=pk)
    if request.method == 'POST':
        form = FollowUpForm(request.POST, instance=fu)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.status == FollowUp.Status.COMPLETED and not obj.completed_at:
                obj.completed_at = timezone.now()
            obj.save()
            messages.success(request, _('پیگیری به‌روزرسانی شد.'))
            return redirect('followups:detail', pk=fu.pk)
    else:
        form = FollowUpForm(instance=fu)
    return render(request, 'followups/form.html', {
        'form': form, 'followup': fu, 'page_title': _('ویرایش پیگیری'), 'is_create': False,
    })
