from django.contrib import admin
from .models import DiagnosisCatalog, EncounterDiagnosis

@admin.register(DiagnosisCatalog)
class DiagnosisCatalogAdmin(admin.ModelAdmin):
    list_display = ('code', 'title_fa', 'title_en', 'category', 'is_active')
    search_fields = ('code', 'title_fa', 'title_en')

@admin.register(EncounterDiagnosis)
class EncounterDiagnosisAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'priority', 'side', 'encounter')
    list_filter = ('priority',)
    raw_id_fields = ('encounter', 'catalog')
