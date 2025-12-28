from django import forms
from django.utils import timezone
from operations.models import Room, Appointment,Review
from accounts.models import Patient, Doctor
from datetime import datetime


class AppointmentForm(forms.ModelForm):
    payment_location = forms.ChoiceField(
        choices=[('platform', 'Pay via Platform (Card)'), ('clinic', 'Pay at Clinic (Cash)')],
        widget=forms.RadioSelect,
        initial='clinic',
        label="Payment Preference"
    )
    date_time = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Appointment
        fields = ['doctor','patient', 'date_time', 'reason', 'payment_location']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional: Reason for visit'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)
        self.fields['doctor'].widget.attrs['class'] = 'form-control-custom w-100'

        self.fields['patient'].queryset = Patient.objects.all()
        self.fields['patient'].widget.attrs['class'] = 'form-control-custom w-100'

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        # المتغير ده هو التاريخ والوقت جاهز، مش محتاج تحويل
        dt_aware = cleaned_data.get('date_time') 
        
        if dt_aware:
            # 1. التأكد إن التاريخ مش قديم
            if dt_aware < timezone.now():
                 raise forms.ValidationError("You cannot book an appointment in the past.")

            # 2. التأكد من إن الدكتور فاضي في الوقت ده
            if doctor:
                if Appointment.objects.filter(doctor=doctor, date_time=dt_aware).exclude(status='Cancelled').exists():
                    raise forms.ValidationError(f"Dr. {doctor.name} is already booked at this time. Please choose another slot.")

            # 3. التأكد إن المريض معندوش حجز تاني في نفس الوقت (لو اليوزر موجود)
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
    