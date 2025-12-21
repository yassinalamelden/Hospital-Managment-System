from django.contrib import admin
from .models import Appointment, Room

class OccupancyFilter(admin.SimpleListFilter):
    title = 'Occupancy Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('occupied', 'Occupied'),
            ('available', 'Available'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'occupied':
            return queryset.filter(current_patient__isnull=False)
        if self.value() == 'available':
            return queryset.filter(current_patient__isnull=True)
        return queryset

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date_time', 'status')
    list_filter = ('status', 'date_time')
    search_fields = ('doctor__name', 'patient__name')
    ordering = ('-date_time',) 

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price_per_night', 'is_occupied_display')
    list_filter = ('room_type', OccupancyFilter, 'admission_date')
    search_fields = ('room_number',)

    def is_occupied_display(self, obj):
        return obj.current_patient is not None
    
    is_occupied_display.boolean = True
    is_occupied_display.short_description = 'Occupied'