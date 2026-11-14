from django.contrib import admin
from .models import Prescription, PrescriptionItem

class ItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'status', 'approved_at')
    inlines = [ItemInline]
    raw_id_fields = ('encounter', 'patient')
