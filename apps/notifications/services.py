"""Notification service — extensible for SMS later."""
from .models import Notification


def notify_user(user, title, body='', category='system', link='', channel='in_app'):
    return Notification.objects.create(
        recipient=user,
        title=title,
        body=body,
        category=category,
        channel=channel,
        link=link,
    )


def notify_appointment_reminder(user, appointment):
    return notify_user(
        user,
        title=f'یادآوری نوبت: {appointment.patient.full_name}',
        body=f'نوبت در {appointment.scheduled_at:%Y-%m-%d %H:%M}',
        category='appointment',
        link='/appointments/',
    )
