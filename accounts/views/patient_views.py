from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from accounts.models import Patient
from accounts.forms import PatientForm

class PatientDashboardView(DetailView):
    model = Patient
    template_name = 'accounts/patient_dashboard.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.get_object()
        context['appointments'] = patient.appointments.all().order_by('-date_time')
        context['bills'] = patient.bills.all().order_by('-issued_date')
        return context

class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'accounts/patient_form.html'
    success_url = reverse_lazy('patient-list')

class PatientListView(ListView):
    model = Patient
    template_name = 'accounts/patient_list.html'
    context_object_name = 'patients'
