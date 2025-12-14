from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from accounts.models import Patient
from accounts.forms import PatientForm

class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'accounts/patient_form.html'
    success_url = reverse_lazy('patient-list')

class PatientListView(ListView):
    model = Patient
    template_name = 'accounts/patient_list.html'
    context_object_name = 'patients'
