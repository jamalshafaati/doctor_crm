from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from .models import Notification


@login_required
def notification_list(request):
    qs = Notification.objects.filter(recipient=request.user)[:50]
    unread = qs.filter(is_read=False).count()
    return render(request, 'notifications/list.html', {
        'notifications': qs,
        'unread_count': unread,
        'page_title': _('اعلان‌ها'),
    })


@login_required
def notification_mark_read(request, pk):
    n = get_object_or_404(Notification, pk=pk, recipient=request.user)
    n.is_read = True
    n.save(update_fields=['is_read'])
    if n.link:
        return redirect(n.link)
    return redirect('notifications:list')


@login_required
def notification_mark_all_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect('notifications:list')
