"""Jalali display + parse helpers. Storage remains Gregorian."""
from __future__ import annotations
import datetime
from typing import Optional, Union

try:
    import jdatetime
except ImportError:
    jdatetime = None


def to_jalali(value: Union[datetime.date, datetime.datetime, None], with_time: bool = False) -> str:
    if value is None:
        return ''
    if jdatetime is None:
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y/%m/%d %H:%M' if with_time else '%Y/%m/%d')
        return value.strftime('%Y/%m/%d')
    if isinstance(value, datetime.datetime):
        j = jdatetime.datetime.fromgregorian(datetime=value)
        return j.strftime('%Y/%m/%d %H:%M' if with_time else '%Y/%m/%d')
    j = jdatetime.date.fromgregorian(date=value)
    return j.strftime('%Y/%m/%d')


def parse_jalali_date(s: str) -> Optional[datetime.date]:
    """Accept 1403/01/15 or 1403-01-15 or Gregorian 2024-03-21."""
    if not s or not str(s).strip():
        return None
    s = str(s).strip().replace('-', '/')
    parts = s.split('/')
    if len(parts) != 3:
        return None
    try:
        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        return None
    # Jalali years are typically 1300-1500
    if y > 1500:
        try:
            return datetime.date(y, m, d)
        except ValueError:
            return None
    if jdatetime is None:
        return None
    try:
        return jdatetime.date(y, m, d).togregorian()
    except Exception:
        return None


def parse_jalali_datetime(date_s: str, time_s: str = '') -> Optional[datetime.datetime]:
    d = parse_jalali_date(date_s)
    if not d:
        return None
    hour, minute = 0, 0
    if time_s:
        tparts = time_s.strip().split(':')
        try:
            hour = int(tparts[0])
            minute = int(tparts[1]) if len(tparts) > 1 else 0
        except (ValueError, IndexError):
            pass
    return datetime.datetime(d.year, d.month, d.day, hour, minute)
