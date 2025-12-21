from django import forms
from django.utils import timezone
from operations.models import Room, Appointment
from accounts.models import Patient, Doctor

class AppointmentForm(forms.ModelForm):
    payment_location = forms.ChoiceField(
        choices=[('platform', 'Pay via Platform (Card)'), ('clinic', 'Pay at Clinic (Cash)')],
        widget=forms.RadioSelect,
        initial='clinic',
        label="Payment Preference"
    )
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date_time', 'reason']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional: Reason for visit'}),
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

        self.fields["current_patient"].queryset = Patient.objects.filter(room__isnull=True)


        if not self.initial.get("admission_date"):
            self.initial["admission_date"] = timezone.localdate()

from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control-custom', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control-custom', 'rows': 3, 'placeholder': 'Share your experience...'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price_per_night']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control-custom'}),
            'room_type': forms.Select(attrs={'class': 'form-control-custom'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control-custom'}),
        }

