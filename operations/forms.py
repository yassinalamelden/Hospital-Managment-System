from django import forms
from django.utils import timezone
from operations.models import Room, Appointment
from accounts.models import Patient, Doctor

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date_time']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class RoomAssignForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["current_patient", "admission_date"]
        widgets = {
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only show patients who are not already assigned to a room
        self.fields["current_patient"].queryset = Patient.objects.filter(room__isnull=True)

        # Default admission date = today
        if not self.initial.get("admission_date"):
            self.initial["admission_date"] = timezone.localdate()
