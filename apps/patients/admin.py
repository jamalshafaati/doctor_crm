from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_number', 'full_name', 'phone', 'gender', 'registered_at', 'is_active')
    list_filter = ('gender', 'is_active')
    search_fields = ('patient_number', 'first_name', 'last_name', 'phone', 'national_id')
    readonly_fields = ('patient_number', 'registered_at', 'updated_at')
