from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone


class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', _('زمان‌بندی شده')
        CONFIRMED = 'confirmed', _('تأیید شده')
        CHECKED_IN = 'checked_in', _('چک‌این شده')
        COMPLETED = 'completed', _('انجام شده')
        CANCELLED = 'cancelled', _('لغو شده')
        NO_SHOW = 'no_show', _('عدم مراجعه')

    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name=_('بیمار')
    )
    doctor = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        related_name='doctor_appointments',
        limit_choices_to={'role': 'doctor'},
        verbose_name=_('پزشک')
    )
    scheduled_at = models.DateTimeField(verbose_name=_('زمان نوبت'), db_index=True)
    duration_minutes = models.PositiveIntegerField(default=30, verbose_name=_('مدت (دقیقه)'))
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
        verbose_name=_('وضعیت')
    )
    reason = models.CharField(max_length=255, blank=True, verbose_name=_('علت مراجعه'))
    notes = models.TextField(blank=True, verbose_name=_('یادداشت'))
    checked_in_at = models.DateTimeField(null=True, blank=True, verbose_name=_('زمان چک‌این'))
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_appointments',
        verbose_name=_('ایجادکننده')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('نوبت')
        verbose_name_plural = _('نوبت‌ها')
        ordering = ['scheduled_at']
        indexes = [
            models.Index(fields=['scheduled_at', 'status']),
            models.Index(fields=['doctor', 'scheduled_at']),
        ]

    def __str__(self):
        return f"{self.patient.full_name} @ {self.scheduled_at:%Y-%m-%d %H:%M}"

    def clean(self):
        """Prevent overlapping appointments for the same doctor."""
        if not self.scheduled_at or not self.doctor_id:
            return
        start = self.scheduled_at
        end = start + timezone.timedelta(minutes=self.duration_minutes or 30)
        qs = Appointment.objects.filter(
            doctor=self.doctor,
            status__in=[
                self.Status.SCHEDULED,
                self.Status.CONFIRMED,
                self.Status.CHECKED_IN,
            ],
        ).exclude(pk=self.pk)
        # Simple overlap check
        for appt in qs:
            appt_end = appt.scheduled_at + timezone.timedelta(minutes=appt.duration_minutes or 30)
            if start < appt_end and end > appt.scheduled_at:
                raise ValidationError(
                    _('این زمان با نوبت دیگری برای این پزشک تداخل دارد.')
                )

    def check_in(self):
        if self.status in [self.Status.CANCELLED, self.Status.COMPLETED, self.Status.NO_SHOW]:
            raise ValidationError(_('نمی‌توان این نوبت را چک‌این کرد.'))
        self.status = self.Status.CHECKED_IN
        self.checked_in_at = timezone.now()
        self.save(update_fields=['status', 'checked_in_at', 'updated_at'])
