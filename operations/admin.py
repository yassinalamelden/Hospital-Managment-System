from django.contrib import admin
from .models import Room, Appointment

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price_per_night', 'is_occupied_display')
    list_filter = ('room_type',)
    search_fields = ('room_number',)

    def is_occupied_display(self, obj):
        return obj.is_occupied
    is_occupied_display.boolean = True
    is_occupied_display.short_description = 'Occupied'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date_time', 'status')
    list_filter = ('status', 'date_time')
    search_fields = ('doctor__name', 'patient__name')
