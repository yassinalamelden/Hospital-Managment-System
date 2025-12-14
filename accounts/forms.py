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
