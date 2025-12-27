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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email address is already in use by another account.")
        return email

class PatientForm(forms.ModelForm):
    COUNTRY_CODES = [
        ('+20', 'Egypt (+20)'),
        ('+966', 'Saudi Arabia (+966)'),
        ('+971', 'UAE (+971)'),
        ('+1', 'USA (+1)'),
        ('+44', 'UK (+44)'),
    ]
    country_code = forms.ChoiceField(choices=COUNTRY_CODES, required=False, label="Code")

    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'gender', 'country_code', 'phone', 'address', 'medical_history', 'blood_type']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            'medical_history': forms.Textarea(attrs={'rows': 2}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control-custom w-100'
        
        # Lock Date of Birth if already set
        if self.instance and self.instance.date_of_birth:
             self.fields['date_of_birth'].widget.attrs['readonly'] = 'readonly'
             self.fields['date_of_birth'].widget.attrs['style'] = 'background-color: #e9ecef; cursor: not-allowed;'
             # Also add a help text or title
             self.fields['date_of_birth'].help_text = "Date of Birth cannot be changed once set."

        # Customize country code and phone for input group
        # Remove w-100 from country_code so it doesn't take full line
        # Add specific spacing/style classes
        self.fields['country_code'].widget.attrs['class'] = 'form-select form-control-custom'
        self.fields['country_code'].widget.attrs['style'] = 'max-width: 150px; border-top-right-radius: 0; border-bottom-right-radius: 0; border-right: 0;'
        
        self.fields['phone'].widget.attrs['class'] = 'form-control form-control-custom'
        self.fields['phone'].widget.attrs['style'] = 'border-top-left-radius: 0; border-bottom-left-radius: 0;'

        # Split existing phone number into code and number
        if self.instance and self.instance.phone and self.instance.phone != 'None':
            # Check if phone starts with any known code
            for code, _ in self.COUNTRY_CODES:
                if self.instance.phone.startswith(code):
                    self.initial['country_code'] = code
                    self.initial['phone'] = self.instance.phone[len(code):]
                    break
            # Default fallback if no code matches (or if manual entry didn't use code)
            
    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        country_code = cleaned_data.get('country_code')
        
        # Enforce Age/DOB locking
        if self.instance.date_of_birth:
            # If already set, ensure it hasn't changed (or ignore new value and keep old)
            # Since field is readonly, browser sends it back. 
            # If user manipulated it, we should revert or error.
            # Let's revert to instance value to be safe/silent, or error.
            # Error is clearer if they try to hack.
            new_dob = cleaned_data.get('date_of_birth')
            if new_dob != self.instance.date_of_birth:
                self.add_error('date_of_birth', "Date of Birth cannot be changed once set.")
        
        if phone and country_code:
            # Validate length based on country code
            # Lengths are based on local format (often including leading zero if that's the standard expectation)
            LENGTH_RULES = {
                '+20': 11,   # Egypt: 01xxxxxxxxx
                '+966': 9,   # Saudi: 5xxxxxxxx (Standard mobile without leading 0, usually 9) or 10?
                             # User asked explicitly for "11 for Egypt". I will assume standard lengths for others.
                             # Saudi mobile: +966 5x xxx xxxx (9 digits)
                '+971': 9,   # UAE: +971 5x xxx xxxx (9 digits)
                '+1': 10,    # USA: 3 area + 7 number (10 digits)
                '+44': 10,   # UK: +44 7xxx xxx xxx (10 digits usually excluding 0)
            }
            
            # Special handling for "0" prefix if user entered it but we expect shorter?
            # Or just strictly check length.
            # User request: "11 number only for egypt"
            
            expected_length = LENGTH_RULES.get(country_code)
            
            # Clean non-digit characters just in case
            if not phone.isdigit():
                 self.add_error('phone', "Phone number must contain only digits.")
            elif expected_length:
                if len(phone) != expected_length:
                    self.add_error('phone', f"For {country_code}, the phone number must be exactly {expected_length} digits.")
            
            # Recombine for saving
            full_phone = f"{country_code}{phone}"
            cleaned_data['phone'] = full_phone
            # Update the instance directly to ensure it propagates
            self.instance.phone = full_phone
            
        # Validation: Name cannot be the same as Username
        name = cleaned_data.get('name')
        if name and self.instance.user:
            if name.lower() == self.instance.user.username.lower():
                 self.add_error('name', "Your Full Name cannot be the same as your Username. Please use your real name.")

        return cleaned_data

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
