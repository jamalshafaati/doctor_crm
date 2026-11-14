from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import uuid


class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = 'male', _('مرد')
        FEMALE = 'female', _('زن')
        OTHER = 'other', _('سایر')

    # Unique human-readable patient number (not phone/national ID)
    patient_number = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        blank=True,
        verbose_name=_('شماره پرونده')
    )
    first_name = models.CharField(max_length=100, verbose_name=_('نام'))
    last_name = models.CharField(max_length=100, verbose_name=_('نام خانوادگی'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('تاریخ تولد'))
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        blank=True,
        verbose_name=_('جنسیت')
    )
    phone = models.CharField(max_length=20, blank=True, db_index=True, verbose_name=_('تلفن'))
    email = models.EmailField(blank=True, verbose_name=_('ایمیل'))
    address = models.TextField(blank=True, verbose_name=_('آدرس'))
    national_id = models.CharField(max_length=20, blank=True, verbose_name=_('کد ملی'))
    emergency_contact_name = models.CharField(max_length=100, blank=True, verbose_name=_('نام تماس اضطراری'))
    emergency_contact_phone = models.CharField(max_length=20, blank=True, verbose_name=_('تلفن اضطراری'))
    notes = models.TextField(blank=True, verbose_name=_('یادداشت‌ها'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ثبت'))
    updated_at = models.DateTimeField(auto_now=True)

    # Optional link to portal account
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patient_record',
        verbose_name=_('حساب کاربری')
    )

    class Meta:
        verbose_name = _('بیمار')
        verbose_name_plural = _('بیماران')
        ordering = ['-registered_at']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f"{self.patient_number} — {self.full_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def save(self, *args, **kwargs):
        if not self.patient_number:
            # Generate sequential-like number: P-YYYYMMDD-XXXX
            from django.utils import timezone
            today = timezone.now().strftime('%Y%m%d')
            last = Patient.objects.filter(patient_number__startswith=f'P-{today}').order_by('-patient_number').first()
            if last:
                try:
                    seq = int(last.patient_number.split('-')[-1]) + 1
                except (ValueError, IndexError):
                    seq = 1
            else:
                seq = 1
            self.patient_number = f'P-{today}-{seq:04d}'
        super().save(*args, **kwargs)
