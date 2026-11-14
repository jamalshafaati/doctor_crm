from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Encounter(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', _('پیش‌نویس')
        IN_PROGRESS = 'in_progress', _('در حال انجام')
        PENDING_REVIEW = 'pending_review', _('در انتظار بررسی')
        FINALIZED = 'finalized', _('نهایی شده')
        AMENDED = 'amended', _('اصلاح شده')

    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='encounters',
        verbose_name=_('بیمار')
    )
    appointment = models.OneToOneField(
        'appointments.Appointment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='encounter',
        verbose_name=_('نوبت مرتبط')
    )
    doctor = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        related_name='encounters',
        limit_choices_to={'role__in': ['doctor', 'admin']},
        verbose_name=_('پزشک')
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_('وضعیت')
    )
    chief_complaint = models.TextField(blank=True, verbose_name=_('شکایت اصلی'))
    started_at = models.DateTimeField(default=timezone.now, verbose_name=_('شروع ویزیت'))
    finalized_at = models.DateTimeField(null=True, blank=True, verbose_name=_('زمان نهایی‌سازی'))
    finalized_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='finalized_encounters',
        verbose_name=_('نهایی‌کننده')
    )
    notes = models.TextField(blank=True, verbose_name=_('یادداشت کلی'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('ویزیت')
        verbose_name_plural = _('ویزیت‌ها')
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['patient', '-started_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Encounter #{self.pk} — {self.patient.full_name} ({self.get_status_display()})"

    @property
    def is_locked(self):
        return self.status in [self.Status.FINALIZED, self.Status.AMENDED]

    def finalize(self, user):
        if self.is_locked:
            raise ValueError(_('این ویزیت قبلاً نهایی شده است.'))
        self.status = self.Status.FINALIZED
        self.finalized_at = timezone.now()
        self.finalized_by = user
        self.save(update_fields=['status', 'finalized_at', 'finalized_by', 'updated_at'])


class EncounterAmendment(models.Model):
    """Controlled amendment of a finalized encounter."""
    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.CASCADE,
        related_name='amendments',
        verbose_name=_('ویزیت')
    )
    previous_content = models.JSONField(verbose_name=_('محتوای قبلی'))
    new_content = models.JSONField(verbose_name=_('محتوای جدید'))
    reason = models.TextField(verbose_name=_('دلیل اصلاح'))
    amended_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        verbose_name=_('اصلاح‌کننده')
    )
    amended_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('اصلاح ویزیت')
        verbose_name_plural = _('اصلاحات ویزیت')
        ordering = ['-amended_at']
