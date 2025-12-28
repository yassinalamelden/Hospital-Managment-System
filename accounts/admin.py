from django.contrib import admin
from .models import Doctor, Patient

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'phone', 'is_active')
    list_filter = ('specialty', 'is_active')
    search_fields = ('name',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'gender', 'blood_type')
    list_filter = ('gender', 'blood_type')
    search_fields = ('name', 'user__username')