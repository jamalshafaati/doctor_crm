from django.contrib import admin
from .models import ImagingStudy
@admin.register(ImagingStudy)
class ImagingStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'category', 'study_date', 'created_at')
    list_filter = ('category',)
    raw_id_fields = ('patient', 'encounter')
