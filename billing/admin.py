from django.contrib import admin
from .models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('patient', 'issued_date', 'total_amount', 'is_paid')
    list_filter = ('is_paid', 'issued_date')
    search_fields = ('patient__name', 'patient__patient_id')
    readonly_fields = ('total_amount',)
