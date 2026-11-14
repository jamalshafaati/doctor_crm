from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from apps.appointments.models import Appointment


@transaction.atomic
def create_appointment(*, patient, doctor, scheduled_at, duration_minutes=30,
                       reason='', notes='', created_by=None) -> Appointment:
    appt = Appointment(
        patient=patient,
        doctor=doctor,
        scheduled_at=scheduled_at,
        duration_minutes=duration_minutes,
        reason=reason,
        notes=notes,
        created_by=created_by,
        status=Appointment.Status.SCHEDULED,
    )
    appt.full_clean()  # includes double-booking check
    appt.save()
    return appt


def check_in_appointment(appointment: Appointment) -> Appointment:
    appointment.check_in()
    return appointment


def cancel_appointment(appointment: Appointment, reason: str = '') -> Appointment:
    if appointment.status in [Appointment.Status.COMPLETED, Appointment.Status.CANCELLED]:
        raise ValidationError('این نوبت قابل لغو نیست.')
    appointment.status = Appointment.Status.CANCELLED
    if reason:
        appointment.notes = (appointment.notes + '\n' + f'لغو: {reason}').strip()
    appointment.save(update_fields=['status', 'notes', 'updated_at'])
    return appointment
