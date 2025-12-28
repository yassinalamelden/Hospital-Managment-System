from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

class ProfileCompletionRequiredMixin(AccessMixin):
    """
    Ensure the user has a complete patient profile before accessing the view.
    Checks:
    - User has a patient profile
    - Age is not 0
    - Gender is not 'Not specified'
    - Phone is not 'None'
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # If user is staff/superuser, bypass checks
        if request.user.is_staff or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if not hasattr(request.user, 'patient'):
            messages.error(request, "Patient profile not found.")
            return redirect('home')

        patient = request.user.patient
        
        # Check for incomplete fields (based on defaults in SignUpView)
        # Check date_of_birth instead of age
        if not patient.date_of_birth or patient.gender == 'Not specified' or patient.phone == 'None':
            messages.warning(request, "Please complete your profile details (Date of Birth, Gender, Phone) to access this feature.")
            return redirect('account-settings')

        return super().dispatch(request, *args, **kwargs)
