from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class TreatmentPlan(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', _('پیش‌نویس')
        FINALIZED = 'finalized', _('نهایی')

    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.CASCADE,
        related_name='treatment_plans', verbose_name=_('ویزیت')
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name=_('وضعیت')
    )
    conservative = models.TextField(blank=True, verbose_name=_('درمان محافظه‌کارانه'))
    physiotherapy = models.TextField(blank=True, verbose_name=_('فیزیوتراپی'))
    immobilization = models.TextField(blank=True, verbose_name=_('ثابت‌سازی'))
    weight_bearing = models.TextField(blank=True, verbose_name=_('دستور تحمل وزن'))
    medication_recommendations = models.TextField(blank=True, verbose_name=_('توصیه دارویی'))
    surgical_consideration = models.TextField(blank=True, verbose_name=_('ملاحظات جراحی'))
    followup_instructions = models.TextField(blank=True, verbose_name=_('دستورات پیگیری'))
    finalized_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='finalized_treatments',
        verbose_name=_('نهایی‌کننده')
    )
    finalized_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('طرح درمان')
        verbose_name_plural = _('طرح‌های درمان')
        ordering = ['-created_at']

    def __str__(self):
        return f"Treatment Plan — Encounter {self.encounter_id} ({self.get_status_display()})"
