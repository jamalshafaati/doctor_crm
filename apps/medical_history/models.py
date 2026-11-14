from django.db import models
from django.utils.translation import gettext_lazy as _


class MedicalHistory(models.Model):
    """One structured medical history record per patient (can be updated)."""
    patient = models.OneToOneField(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='medical_history',
        verbose_name=_('بیمار')
    )
    past_medical_history = models.TextField(blank=True, verbose_name=_('سابقه پزشکی'))
    past_surgical_history = models.TextField(blank=True, verbose_name=_('سابقه جراحی'))
    current_medications = models.TextField(blank=True, verbose_name=_('داروهای فعلی'))
    family_history = models.TextField(blank=True, verbose_name=_('سابقه خانوادگی'))
    social_history = models.TextField(blank=True, verbose_name=_('سابقه اجتماعی'))
    previous_injuries = models.TextField(blank=True, verbose_name=_('آسیب‌های قبلی'))
    previous_foot_ankle_treatments = models.TextField(blank=True, verbose_name=_('درمان‌های قبلی پا و مچ پا'))
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('آخرین ویرایش‌کننده')
    )

    class Meta:
        verbose_name = _('سابقه پزشکی')
        verbose_name_plural = _('سوابق پزشکی')

    def __str__(self):
        return f"History — {self.patient.full_name}"


class Allergy(models.Model):
    class Severity(models.TextChoices):
        MILD = 'mild', _('خفیف')
        MODERATE = 'moderate', _('متوسط')
        SEVERE = 'severe', _('شدید')

    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='allergies',
        verbose_name=_('بیمار')
    )
    allergen = models.CharField(max_length=200, verbose_name=_('آلرژن'))
    reaction = models.CharField(max_length=255, blank=True, verbose_name=_('واکنش'))
    severity = models.CharField(
        max_length=20,
        choices=Severity.choices,
        default=Severity.MODERATE,
        verbose_name=_('شدت')
    )
    notes = models.TextField(blank=True, verbose_name=_('یادداشت'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('آلرژی')
        verbose_name_plural = _('آلرژی‌ها')
        ordering = ['-severity', 'allergen']

    def __str__(self):
        return f"{self.allergen} ({self.get_severity_display()})"


class ClinicalAlert(models.Model):
    """Important clinical alerts shown prominently on patient chart."""
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='alerts',
        verbose_name=_('بیمار')
    )
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    description = models.TextField(blank=True, verbose_name=_('توضیحات'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('ایجادکننده')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('هشدار بالینی')
        verbose_name_plural = _('هشدارهای بالینی')
        ordering = ['-created_at']
