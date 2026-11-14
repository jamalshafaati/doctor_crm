from django.db.models import Q
from .models import Patient


def create_patient(**kwargs):
    patient = Patient(**kwargs)
    patient.save()
    return patient


def update_patient(patient, **kwargs):
    for k, v in kwargs.items():
        setattr(patient, k, v)
    patient.save()
    return patient


def search_patients(query='', gender=None, has_surgery=None, has_allergy=None, is_active=True):
    qs = Patient.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    if query:
        q = query.strip()
        qs = qs.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(patient_number__icontains=q) |
            Q(phone__icontains=q) |
            Q(national_id__icontains=q) |
            Q(email__icontains=q)
        )
    if gender:
        qs = qs.filter(gender=gender)
    if has_surgery is True:
        qs = qs.filter(surgeries__isnull=False).distinct()
    elif has_surgery is False:
        qs = qs.filter(surgeries__isnull=True)
    if has_allergy is True:
        qs = qs.filter(allergies__is_active=True).distinct()
    return qs.order_by('-registered_at')
