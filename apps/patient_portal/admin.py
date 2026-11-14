from django.contrib import admin
from .models import PublishedDocument, AppointmentRequest

@admin.register(PublishedDocument)
class PublishedDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'doc_type', 'is_published', 'published_at')
    list_filter = ('doc_type', 'is_published')
    raw_id_fields = ('patient', 'encounter')

@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'preferred_date', 'status', 'created_at')
    list_filter = ('status',)
