from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.clinical.models import Side


class FollowUp(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', _('زمان‌بندی شده')
        COMPLETED = 'completed', _('انجام شده')
        MISSED = 'missed', _('از دست رفته')
        CANCELLED = 'cancelled', _('لغو شده')

    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE,
        related_name='followups', verbose_name=_('بیمار')
    )
    surgery = models.ForeignKey(
        'surgery.Surgery', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='followups', verbose_name=_('جراحی مرتبط')
    )
    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='followups', verbose_name=_('ویزیت مرتبط')
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='followups', limit_choices_to={'role__in': ['doctor', 'admin']},
        verbose_name=_('پزشک')
    )
    scheduled_date = models.DateField(verbose_name=_('تاریخ پیگیری'))
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SCHEDULED, verbose_name=_('وضعیت')
    )
    # Clinical assessment at follow-up
    pain_score = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name=_('نمره درد (۰–۱۰)')
    )
    wound_status = models.CharField(max_length=100, blank=True, verbose_name=_('وضعیت زخم'))
    mobility = models.CharField(max_length=100, blank=True, verbose_name=_('تحرک'))
    weight_bearing_status = models.CharField(max_length=100, blank=True, verbose_name=_('وضعیت تحمل وزن'))
    rehabilitation_progress = models.TextField(blank=True, verbose_name=_('پیشرفت توانبخشی'))
    complications = models.TextField(blank=True, verbose_name=_('عوارض'))
    side = models.CharField(max_length=20, choices=Side.choices, default=Side.NA, verbose_name=_('طرف'))
    assessment_notes = models.TextField(blank=True, verbose_name=_('یادداشت ارزیابی'))
    next_followup_date = models.DateField(null=True, blank=True, verbose_name=_('تاریخ پیگیری بعدی'))
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_('زمان انجام'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('پیگیری')
        verbose_name_plural = _('پیگیری‌ها')
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"Follow-up {self.scheduled_date} — {self.patient.full_name}"
