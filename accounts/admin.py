from django.contrib import admin
from .models import Doctor, Patient

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'is_active', 'phone')
    search_fields = ('name', 'doctor_id')
    list_filter = ('specialty', 'is_active')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'blood_type', 'phone')
    search_fields = ('name', 'patient_id')
    list_filter = ('blood_type', 'gender')
