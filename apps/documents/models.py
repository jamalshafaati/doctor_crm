import uuid
import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def patient_document_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    name = f"{uuid.uuid4().hex}{ext}"
    return f"private/documents/{instance.patient_id}/{name}"


class PatientDocument(models.Model):
    class Category(models.TextChoices):
        REFERRAL = 'referral', _('معرفی‌نامه')
        LAB = 'lab', _('آزمایش')
        IMAGING = 'imaging', _('تصویربرداری')
        CONSENT = 'consent', _('رضایت‌نامه')
        INSURANCE = 'insurance', _('بیمه')
        REPORT = 'report', _('گزارش')
        OTHER = 'other', _('سایر')

    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE,
        related_name='documents', verbose_name=_('بیمار')
    )
    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='documents', verbose_name=_('ویزیت')
    )
    title = models.CharField(max_length=255, verbose_name=_('عنوان'))
    category = models.CharField(
        max_length=30, choices=Category.choices, default=Category.OTHER, verbose_name=_('دسته')
    )
    description = models.TextField(blank=True, verbose_name=_('توضیحات'))
    file = models.FileField(upload_to=patient_document_path, verbose_name=_('فایل'))
    original_filename = models.CharField(max_length=255, blank=True, verbose_name=_('نام اصلی'))
    content_type = models.CharField(max_length=100, blank=True)
    file_size = models.PositiveIntegerField(default=0)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name=_('آپلودکننده')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('سند بیمار')
        verbose_name_plural = _('اسناد بیمار')
        ordering = ['-created_at']

    def __str__(self):
        return self.title
