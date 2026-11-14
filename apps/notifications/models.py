from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Notification(models.Model):
    class Channel(models.TextChoices):
        IN_APP = 'in_app', _('داخل سیستم')
        SMS = 'sms', _('پیامک')  # integration point
        EMAIL = 'email', _('ایمیل')

    class Category(models.TextChoices):
        APPOINTMENT = 'appointment', _('نوبت')
        FOLLOWUP = 'followup', _('پیگیری')
        SYSTEM = 'system', _('سیستم')
        CLINICAL = 'clinical', _('بالینی')

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='notifications', verbose_name=_('گیرنده')
    )
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    body = models.TextField(blank=True, verbose_name=_('متن'))
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.SYSTEM, verbose_name=_('دسته')
    )
    channel = models.CharField(
        max_length=20, choices=Channel.choices, default=Channel.IN_APP, verbose_name=_('کانال')
    )
    is_read = models.BooleanField(default=False, verbose_name=_('خوانده‌شده'))
    link = models.CharField(max_length=255, blank=True, verbose_name=_('لینک'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('اعلان')
        verbose_name_plural = _('اعلان‌ها')
        ordering = ['-created_at']

    def __str__(self):
        return self.title
