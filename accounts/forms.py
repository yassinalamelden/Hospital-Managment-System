from django import forms
from django.contrib.auth.models import User
from .models import Doctor, Patient

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'age', 'gender', 'phone', 'address', 'specialty', 'is_active']
        widgets = {
            'is_active': forms.RadioSelect(choices=[(True, 'Active'), (False, 'Inactive')])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs['class'] = 'form-control'
        
        # Specific styling for radio select if needed, usually done in template or via wrapper classes
        # But we can leave the class off the input itself if we want standard radio behavior


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control-custom w-100'}))

    class Meta:
        model = User
        fields = ['email']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'phone', 'address', 'medical_history', 'blood_type']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            'medical_history': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control-custom w-100'

from operations.models import Appointment

class AppointmentForm(forms.ModelForm):
    PAYMENT_LOCATION_CHOICES = [
        ('platform', 'Pay on the Platform'),
        ('counter', 'Pay at the Counter'),
    ]
    
    TIME_SLOTS = [
        ('09:00', '09:00 AM'), ('10:00', '10:00 AM'), ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'), ('13:00', '01:00 PM'), ('14:00', '02:00 PM'),
        ('15:00', '03:00 PM'), ('16:00', '04:00 PM'), ('17:00', '05:00 PM'),
    ]

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control-custom w-100'}),
        label="Preferred Date"
    )
    time_slot = forms.ChoiceField(
        choices=TIME_SLOTS,
        widget=forms.Select(attrs={'class': 'form-control-custom w-100'}),
        label="Time Slot"
    )
    
    payment_location = forms.ChoiceField(
        choices=PAYMENT_LOCATION_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control-custom w-100'}),
        label="Where would you like to pay?"
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'reason', 'payment_location'] # date_time excluded, handled in view
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control-custom w-100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)
        self.fields['doctor'].widget.attrs['class'] = 'form-control-custom w-100'
