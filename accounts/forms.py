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
    PAYMENT_LOCATION_CHOICES = [
        ('platform', 'Pay on the Platform'),
        ('counter', 'Pay at the Counter'),
    ]
    
    payment_location = forms.ChoiceField(
        choices=PAYMENT_LOCATION_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control-custom w-100'}),
        label="Where would you like to pay?"
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'reason', 'payment_location']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control-custom w-100',
                'placeholder': f'Select {field.label}'
            })
