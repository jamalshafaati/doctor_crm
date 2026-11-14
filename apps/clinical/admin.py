from django.contrib import admin
from .models import ClinicalExamination
@admin.register(ClinicalExamination)
class ClinicalExaminationAdmin(admin.ModelAdmin):
    list_display = ('id', 'encounter', 'side', 'pain_severity', 'created_at')
    raw_id_fields = ('encounter',)
