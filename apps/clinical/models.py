"""
General clinical examination records attached to an Encounter.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Side(models.TextChoices):
    RIGHT = 'right', _('راست')
    LEFT = 'left', _('چپ')
    BILATERAL = 'bilateral', _('دو طرفه')
    NA = 'na', _('نامشخص')


class ClinicalExamination(models.Model):
    """General examination for a visit."""
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='clinical_exams',
        verbose_name=_('ویزیت')
    )
    # History of present illness
    chief_complaint = models.TextField(blank=True, verbose_name=_('شکایت اصلی'))
    onset = models.CharField(max_length=100, blank=True, verbose_name=_('شروع'))
    duration = models.CharField(max_length=100, blank=True, verbose_name=_('مدت'))
    mechanism_of_injury = models.TextField(blank=True, verbose_name=_('مکانیسم آسیب'))
    pain_location = models.CharField(max_length=200, blank=True, verbose_name=_('محل درد'))
    pain_severity = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name=_('شدت درد (۰–۱۰)')
    )
    pain_character = models.CharField(max_length=100, blank=True, verbose_name=_('ماهیت درد'))
    aggravating_factors = models.TextField(blank=True, verbose_name=_('عوامل تشدیدکننده'))
    relieving_factors = models.TextField(blank=True, verbose_name=_('عوامل تسکین‌دهنده'))
    functional_limitations = models.TextField(blank=True, verbose_name=_('محدودیت عملکردی'))
    previous_treatment = models.TextField(blank=True, verbose_name=_('درمان قبلی'))

    # Physical exam
    inspection = models.TextField(blank=True, verbose_name=_('مشاهده'))
    palpation = models.TextField(blank=True, verbose_name=_('لمس'))
    range_of_motion = models.TextField(blank=True, verbose_name=_('دامنه حرکتی'))
    stability = models.TextField(blank=True, verbose_name=_('ثبات'))
    muscle_strength = models.TextField(blank=True, verbose_name=_('قدرت عضلانی'))
    neurovascular = models.TextField(blank=True, verbose_name=_('معاینه عصبی-عروقی'))
    gait = models.TextField(blank=True, verbose_name=_('راه رفتن'))
    functional_assessment = models.TextField(blank=True, verbose_name=_('ارزیابی عملکردی'))

    side = models.CharField(max_length=20, choices=Side.choices, default=Side.NA, verbose_name=_('طرف'))
    notes = models.TextField(blank=True, verbose_name=_('یادداشت'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('معاینه بالینی عمومی')
        verbose_name_plural = _('معاینات بالینی عمومی')
        ordering = ['-created_at']

    def __str__(self):
        return f"Exam #{self.pk} — Encounter {self.encounter_id}"
