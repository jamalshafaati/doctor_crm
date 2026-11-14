from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.clinical.models import Side


class Surgery(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'planned', _('برنامه‌ریزی شده')
        COMPLETED = 'completed', _('انجام شده')
        CANCELLED = 'cancelled', _('لغو شده')

    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE,
        related_name='surgeries', verbose_name=_('بیمار')
    )
    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='surgeries', verbose_name=_('ویزیت مرتبط')
    )
    surgeon = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='surgeries_performed', limit_choices_to={'role__in': ['doctor', 'admin']},
        verbose_name=_('جراح')
    )
    procedure = models.CharField(max_length=255, verbose_name=_('نام عمل'))
    surgery_date = models.DateField(verbose_name=_('تاریخ عمل'))
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PLANNED, verbose_name=_('وضعیت')
    )
    side = models.CharField(max_length=20, choices=Side.choices, default=Side.NA, verbose_name=_('طرف'))
    preoperative_diagnosis = models.TextField(blank=True, verbose_name=_('تشخیص قبل از عمل'))
    postoperative_diagnosis = models.TextField(blank=True, verbose_name=_('تشخیص بعد از عمل'))
    indication = models.TextField(blank=True, verbose_name=_('اندیکاسیون'))
    procedure_description = models.TextField(blank=True, verbose_name=_('شرح عمل'))
    anesthesia = models.CharField(max_length=100, blank=True, verbose_name=_('نوع بیهوشی'))
    complications = models.TextField(blank=True, verbose_name=_('عوارض'))
    postoperative_instructions = models.TextField(blank=True, verbose_name=_('دستورات بعد از عمل'))
    surgical_notes = models.TextField(blank=True, verbose_name=_('یادداشت جراحی'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='created_surgeries', verbose_name=_('ایجادکننده')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('جراحی')
        verbose_name_plural = _('جراحی‌ها')
        ordering = ['-surgery_date']

    def __str__(self):
        return f"{self.procedure} — {self.patient.full_name} ({self.surgery_date})"


class Implant(models.Model):
    surgery = models.ForeignKey(
        Surgery, on_delete=models.CASCADE, related_name='implants', verbose_name=_('جراحی')
    )
    name = models.CharField(max_length=200, verbose_name=_('نام ایمپلنت'))
    manufacturer = models.CharField(max_length=150, blank=True, verbose_name=_('سازنده'))
    catalog_number = models.CharField(max_length=100, blank=True, verbose_name=_('شماره کاتالوگ'))
    size = models.CharField(max_length=50, blank=True, verbose_name=_('سایز'))
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name=_('تعداد'))
    notes = models.TextField(blank=True, verbose_name=_('یادداشت'))

    class Meta:
        verbose_name = _('ایمپلنت')
        verbose_name_plural = _('ایمپلنت‌ها')

    def __str__(self):
        return self.name
