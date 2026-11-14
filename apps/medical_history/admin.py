from django.contrib import admin
from .models import MedicalHistory, Allergy, ClinicalAlert

@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'updated_at')
    raw_id_fields = ('patient',)

@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'allergen', 'severity', 'is_active')
    list_filter = ('severity', 'is_active')

@admin.register(ClinicalAlert)
class ClinicalAlertAdmin(admin.ModelAdmin):
    list_display = ('patient', 'title', 'is_active', 'created_at')
