from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.models.patient import Patient
from accounts.forms import PatientForm

# استدعاء المودلز من التطبيقات التانية عشان الداشبورد
from operations.models import Appointment
from billing.models import Bill

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class PatientCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'accounts/patient_form.html'
    success_url = reverse_lazy('patient-list')

class PatientListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Patient
    template_name = 'accounts/patient_list.html'
    context_object_name = 'patients'

class PatientDashboardView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Patient
    template_name = 'accounts/patient_dashboard.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.get_object()
        
        context['appointments'] = Appointment.objects.filter(patient=patient).order_by('-date_time')
        context['bills'] = Bill.objects.filter(patient=patient).order_by('-issued_date')
        
        return context