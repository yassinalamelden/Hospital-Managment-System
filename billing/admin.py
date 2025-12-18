from django.contrib import admin
from .models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('patient', 'issued_date', 'total_amount', 'payment_status', 'is_paid')
    list_filter = ('payment_status', 'issued_date')
    search_fields = ('patient__name',)
    readonly_fields = ('total_amount',)
