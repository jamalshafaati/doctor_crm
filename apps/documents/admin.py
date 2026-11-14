from django.contrib import admin
from .models import PatientDocument
@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'category', 'created_at')
    list_filter = ('category',)
    raw_id_fields = ('patient', 'encounter')
