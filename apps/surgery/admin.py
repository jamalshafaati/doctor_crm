from django.contrib import admin
from .models import Surgery, Implant

class ImplantInline(admin.TabularInline):
    model = Implant
    extra = 0

@admin.register(Surgery)
class SurgeryAdmin(admin.ModelAdmin):
    list_display = ('procedure', 'patient', 'surgeon', 'surgery_date', 'status')
    list_filter = ('status',)
    raw_id_fields = ('patient', 'surgeon', 'encounter')
    inlines = [ImplantInline]
