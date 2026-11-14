import uuid
import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def private_upload_path(instance, filename):
    """Randomized private storage path — never expose original name."""
    ext = os.path.splitext(filename)[1].lower()
    name = f"{uuid.uuid4().hex}{ext}"
    return f"private/imaging/{instance.patient_id}/{name}"


class ImagingStudy(models.Model):
    class Category(models.TextChoices):
        XRAY = 'xray', _('رادیوگرافی')
        MRI = 'mri', _('MRI')
        CT = 'ct', _('CT')
        ULTRASOUND = 'ultrasound', _('سونوگرافی')
        OTHER = 'other', _('سایر')

    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE,
        related_name='imaging_studies', verbose_name=_('بیمار')
    )
    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='imaging_studies',
        verbose_name=_('ویزیت')
    )
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.XRAY, verbose_name=_('دسته')
    )
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    description = models.TextField(blank=True, verbose_name=_('توضیحات'))
    file = models.FileField(upload_to=private_upload_path, verbose_name=_('فایل'))
    original_filename = models.CharField(max_length=255, blank=True, verbose_name=_('نام اصلی فایل'))
    content_type = models.CharField(max_length=100, blank=True, verbose_name=_('نوع فایل'))
    file_size = models.PositiveIntegerField(default=0, verbose_name=_('حجم (بایت)'))
    study_date = models.DateField(null=True, blank=True, verbose_name=_('تاریخ تصویر'))
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name=_('آپلودکننده')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('مطالعه تصویربرداری')
        verbose_name_plural = _('مطالعات تصویربرداری')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.patient.full_name}"
