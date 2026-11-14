from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'scheduled_at', 'status', 'duration_minutes')
    list_filter = ('status', 'scheduled_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'patient__patient_number')
    raw_id_fields = ('patient', 'doctor')
