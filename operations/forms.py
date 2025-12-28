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
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time_slot = forms.CharField(widget=forms.TextInput(attrs={'type': 'time'}))

    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time_slot', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional: Reason for visit'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)
        self.fields['doctor'].widget.attrs['class'] = 'form-control-custom w-100'

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')
        
        if date and time_slot:
            import datetime
            from django.utils import timezone
            
            # Combine date and time
            try:
                hour, minute = map(int, time_slot.split(':'))
                time_obj = datetime.time(hour, minute)
                dt = datetime.datetime.combine(date, time_obj)
                dt_aware = timezone.make_aware(dt)
                cleaned_data['date_time'] = dt_aware # Add combined datetime to cleaned_data
            except ValueError:
                # Should be caught by field validation, but just in case
                raise forms.ValidationError("Invalid time format.")
            
            # Check for past dates
            if dt_aware < timezone.now():
                 raise forms.ValidationError("You cannot book an appointment in the past.")

            # Check Doctor Availability
            if doctor:
                # Check strict equality (same slot)
                if Appointment.objects.filter(doctor=doctor, date_time=dt_aware).exclude(status='Cancelled').exists():
                    raise forms.ValidationError(f"Dr. {doctor.name} is already booked at this time. Please choose another slot.")

            # Check Patient Availability (Double Booking)
            if self.user and hasattr(self.user, 'patient'):
                patient = self.user.patient
                if Appointment.objects.filter(patient=patient, date_time=dt_aware).exclude(status='Cancelled').exists():
                     raise forms.ValidationError("You already have an appointment scheduled for this time.")
        
        return cleaned_data

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
    