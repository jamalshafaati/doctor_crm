from django.db.models import Q
from apps.patients.models import Patient


def create_patient(**data) -> Patient:
    patient = Patient(**data)
    # patient_number is auto-generated in save()
    patient.save()
    return patient


def update_patient(patient: Patient, **data) -> Patient:
    for key, value in data.items():
        if hasattr(patient, key) and key not in ('id', 'patient_number', 'registered_at'):
            setattr(patient, key, value)
    patient.save()
    return patient


def search_patients(query: str = '', gender: str = None, is_active: bool = True):
    qs = Patient.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    if gender:
        qs = qs.filter(gender=gender)
    if query:
        qs = qs.filter(
            Q(patient_number__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(national_id__icontains=query)
        )
    return qs.order_by('-registered_at')
