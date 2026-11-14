from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Prescription(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', _('پیش‌نویس')
        APPROVED = 'approved', _('تأیید شده')
        CANCELLED = 'cancelled', _('لغو شده')

    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.CASCADE,
        related_name='prescriptions', verbose_name=_('ویزیت')
    )
    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE,
        related_name='prescriptions', verbose_name=_('بیمار')
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name=_('وضعیت')
    )
    notes = models.TextField(blank=True, verbose_name=_('توضیحات کلی'))
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='approved_prescriptions',
        verbose_name=_('تأییدکننده')
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('نسخه')
        verbose_name_plural = _('نسخه‌ها')
        ordering = ['-created_at']

    def __str__(self):
        return f"Rx #{self.pk} — {self.patient.full_name}"


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE,
        related_name='items', verbose_name=_('نسخه')
    )
    medication_name = models.CharField(max_length=200, verbose_name=_('نام دارو'))
    dosage = models.CharField(max_length=100, blank=True, verbose_name=_('دوز'))
    frequency = models.CharField(max_length=100, blank=True, verbose_name=_('تکرار'))
    duration = models.CharField(max_length=100, blank=True, verbose_name=_('مدت'))
    route = models.CharField(max_length=50, blank=True, verbose_name=_('راه مصرف'))
    instructions = models.TextField(blank=True, verbose_name=_('دستور مصرف'))
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = _('قلم نسخه')
        verbose_name_plural = _('اقلام نسخه')
        ordering = ['order', 'id']

    def __str__(self):
        return self.medication_name
