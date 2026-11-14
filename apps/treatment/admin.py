from django.contrib import admin
from .models import TreatmentPlan
@admin.register(TreatmentPlan)
class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'encounter', 'status', 'finalized_at')
    raw_id_fields = ('encounter',)
