from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class PublishedDocument(models.Model):
    """
    Doctor-controlled publication of clinical documents to the patient portal.
    Only published items are visible to the patient.
    """
    class DocType(models.TextChoices):
        VISIT_SUMMARY = 'visit_summary', _('خلاصه ویزیت')
        PRESCRIPTION = 'prescription', _('نسخه')
        TREATMENT_PLAN = 'treatment_plan', _('طرح درمان')
        SURGERY_REPORT = 'surgery_report', _('گزارش جراحی')
        LAB_RESULT = 'lab_result', _('نتیجه آزمایش')
        OTHER = 'other', _('سایر')

    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE,
        related_name='published_documents', verbose_name=_('بیمار')
    )
    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='published_docs', verbose_name=_('ویزیت')
    )
    doc_type = models.CharField(max_length=30, choices=DocType.choices, verbose_name=_('نوع'))
    title = models.CharField(max_length=255, verbose_name=_('عنوان'))
    content = models.TextField(blank=True, verbose_name=_('محتوا'))
    # Optional link to underlying clinical objects (by id, loose coupling)
    related_object_type = models.CharField(max_length=50, blank=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    is_published = models.BooleanField(default=True, verbose_name=_('منتشر شده'))
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name=_('منتشرکننده')
    )
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('سند منتشرشده')
        verbose_name_plural = _('اسناد منتشرشده')
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.title} — {self.patient.full_name}"


class AppointmentRequest(models.Model):
    """Patient-initiated appointment request (not a confirmed appointment)."""
    class Status(models.TextChoices):
        PENDING = 'pending', _('در انتظار بررسی')
        APPROVED = 'approved', _('تأیید شده')
        REJECTED = 'rejected', _('رد شده')
        CANCELLED = 'cancelled', _('لغو شده')

    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE,
        related_name='appointment_requests', verbose_name=_('بیمار')
    )
    preferred_date = models.DateField(verbose_name=_('تاریخ ترجیحی'))
    preferred_time = models.TimeField(null=True, blank=True, verbose_name=_('ساعت ترجیحی'))
    reason = models.TextField(blank=True, verbose_name=_('علت مراجعه'))
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_('وضعیت')
    )
    staff_notes = models.TextField(blank=True, verbose_name=_('یادداشت پرسنل'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('درخواست نوبت')
        verbose_name_plural = _('درخواست‌های نوبت')
        ordering = ['-created_at']
