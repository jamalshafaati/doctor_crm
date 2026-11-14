from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model.
    Roles are determined by presence of related profiles or explicit role field.
    """
    class Role(models.TextChoices):
        DOCTOR = 'doctor', _('پزشک')
        RECEPTIONIST = 'receptionist', _('پذیرش')
        PATIENT = 'patient', _('بیمار')
        ADMIN = 'admin', _('مدیر سیستم')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.RECEPTIONIST,
        verbose_name=_('نقش')
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name=_('تلفن'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_doctor(self):
        return self.role == self.Role.DOCTOR

    @property
    def is_receptionist(self):
        return self.role == self.Role.RECEPTIONIST

    @property
    def is_patient(self):
        return self.role == self.Role.PATIENT


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name=_('کاربر')
    )
    medical_license_number = models.CharField(max_length=50, blank=True, verbose_name=_('شماره نظام پزشکی'))
    specialty = models.CharField(max_length=100, default='جراحی پا و مچ پا', verbose_name=_('تخصص'))
    bio = models.TextField(blank=True, verbose_name=_('بیوگرافی'))
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True, verbose_name=_('امضا'))

    class Meta:
        verbose_name = _('پروفایل پزشک')
        verbose_name_plural = _('پروفایل‌های پزشک')

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"


class StaffProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='staff_profile',
        verbose_name=_('کاربر')
    )
    position = models.CharField(max_length=100, blank=True, verbose_name=_('سمت'))

    class Meta:
        verbose_name = _('پروفایل پرسنل')
        verbose_name_plural = _('پروفایل‌های پرسنل')

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class PatientAccount(models.Model):
    """
    Optional portal account for a Patient.
    Linked later to the main Patient model.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_account',
        verbose_name=_('کاربر')
    )

    class Meta:
        verbose_name = _('حساب بیمار')
        verbose_name_plural = _('حساب‌های بیمار')

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class ClinicSettings(models.Model):
    """
    Singleton-like clinic configuration.
    Managed from Settings page.
    """
    name_fa = models.CharField(max_length=200, default='کلینیک تخصصی پا و مچ پا', verbose_name=_('نام کلینیک (فارسی)'))
    name_en = models.CharField(max_length=200, default='Foot & Ankle Specialist Clinic', verbose_name=_('نام کلینیک (انگلیسی)'))
    address = models.TextField(blank=True, verbose_name=_('آدرس'))
    phone = models.CharField(max_length=30, blank=True, verbose_name=_('تلفن'))
    email = models.EmailField(blank=True, verbose_name=_('ایمیل'))
    logo = models.ImageField(upload_to='clinic/', blank=True, null=True, verbose_name=_('لوگو'))
    working_hours = models.CharField(max_length=200, blank=True, verbose_name=_('ساعات کاری'))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('تنظیمات کلینیک')
        verbose_name_plural = _('تنظیمات کلینیک')

    def __str__(self):
        return self.name_fa

    def save(self, *args, **kwargs):
        # Keep only one instance
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
