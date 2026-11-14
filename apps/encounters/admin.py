from django.contrib import admin
from .models import Encounter, EncounterAmendment

@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'status', 'started_at', 'finalized_at')
    list_filter = ('status',)
    search_fields = ('patient__first_name', 'patient__last_name', 'patient__patient_number')
    raw_id_fields = ('patient', 'doctor', 'appointment')

@admin.register(EncounterAmendment)
class EncounterAmendmentAdmin(admin.ModelAdmin):
    list_display = ('encounter', 'amended_by', 'amended_at')
    raw_id_fields = ('encounter', 'amended_by')
