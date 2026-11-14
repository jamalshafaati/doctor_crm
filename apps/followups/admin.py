from django.contrib import admin
from .models import FollowUp

@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ('patient', 'scheduled_date', 'doctor', 'status', 'pain_score')
    list_filter = ('status',)
    raw_id_fields = ('patient', 'doctor', 'surgery', 'encounter')
