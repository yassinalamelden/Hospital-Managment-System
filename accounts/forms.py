from django import forms
from .models import Doctor, Patient

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'age', 'gender', 'phone', 'address', 'specialty', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'phone', 'address', 'medical_history', 'blood_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

from operations.models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'reason']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
