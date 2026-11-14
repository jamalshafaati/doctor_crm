from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.clinical.models import Side


class DiagnosisCatalog(models.Model):
    """Extensible diagnosis catalog (ICD-friendly)."""
    code = models.CharField(max_length=20, blank=True, db_index=True, verbose_name=_('کد'))
    title_fa = models.CharField(max_length=255, verbose_name=_('عنوان فارسی'))
    title_en = models.CharField(max_length=255, blank=True, verbose_name=_('عنوان انگلیسی'))
    category = models.CharField(max_length=100, blank=True, verbose_name=_('دسته'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))

    class Meta:
        verbose_name = _('تشخیص (کاتالوگ)')
        verbose_name_plural = _('کاتالوگ تشخیص‌ها')
        ordering = ['title_fa']

    def __str__(self):
        return f"{self.code} — {self.title_fa}" if self.code else self.title_fa


class EncounterDiagnosis(models.Model):
    class Priority(models.TextChoices):
        PRIMARY = 'primary', _('اصلی')
        SECONDARY = 'secondary', _('فرعی')

    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.CASCADE,
        related_name='diagnoses', verbose_name=_('ویزیت')
    )
    catalog = models.ForeignKey(
        DiagnosisCatalog, on_delete=models.PROTECT,
        null=True, blank=True, related_name='encounter_links',
        verbose_name=_('از کاتالوگ')
    )
    # Free-text fallback / override
    title = models.CharField(max_length=255, verbose_name=_('عنوان تشخیص'))
    code = models.CharField(max_length=20, blank=True, verbose_name=_('کد'))
    priority = models.CharField(
        max_length=20, choices=Priority.choices, default=Priority.PRIMARY, verbose_name=_('اولویت')
    )
    side = models.CharField(max_length=20, choices=Side.choices, default=Side.NA, verbose_name=_('طرف'))
    clinical_notes = models.TextField(blank=True, verbose_name=_('یادداشت بالینی'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('تشخیص ویزیت')
        verbose_name_plural = _('تشخیص‌های ویزیت')
        ordering = ['priority', 'created_at']

    def __str__(self):
        return f"{self.get_priority_display()}: {self.title}"
