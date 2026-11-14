from django import template
from django.utils.translation import get_language
from django.utils import timezone as dj_tz
import datetime
from apps.core.dates import to_jalali

register = template.Library()


@register.filter(name='clinic_date')
def clinic_date(value, arg='short'):
    if value is None or value == '':
        return '—'
    lang = get_language() or 'fa'
    with_time = arg == 'datetime'
    if lang.startswith('fa'):
        return to_jalali(value, with_time=with_time) or '—'
    if isinstance(value, datetime.datetime):
        if dj_tz.is_aware(value):
            value = dj_tz.localtime(value)
        return value.strftime('%Y/%m/%d %H:%M' if with_time else '%Y/%m/%d')
    if isinstance(value, datetime.date):
        return value.strftime('%Y/%m/%d')
    return str(value)


@register.filter(name='clinic_datetime')
def clinic_datetime(value):
    return clinic_date(value, 'datetime')


@register.simple_tag
def jalali_input_value(value):
    """Value for text input showing Jalali date."""
    if not value:
        return ''
    return to_jalali(value, with_time=False)
