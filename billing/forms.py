from django import forms
from .models import Bill

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['patient', 'room_charges', 'doctor_fees', 'medicine_cost', 'is_paid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
