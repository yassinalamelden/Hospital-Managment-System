from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import Doctor, Patient
from .forms import DoctorForm, PatientForm

class DoctorCreateView(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'accounts/doctor_form.html'
    success_url = reverse_lazy('doctor-list')

class DoctorListView(ListView):
    model = Doctor
    template_name = 'accounts/doctor_list.html'
    context_object_name = 'doctors'

class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'accounts/patient_form.html'
    success_url = reverse_lazy('patient-list')

class PatientListView(ListView):
    model = Patient
    template_name = 'accounts/patient_list.html'
    context_object_name = 'patients'
