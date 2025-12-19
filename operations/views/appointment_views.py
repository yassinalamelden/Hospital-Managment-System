from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from operations.models import Appointment
from operations.forms import AppointmentForm

class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'operations/appointment_form.html'
    success_url = reverse_lazy('appointment-list')

class AppointmentListView(ListView):
    model = Appointment
    template_name = 'operations/appointment_list.html'
    context_object_name = 'appointments'

class AppointmentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Appointment
    template_name = 'operations/appointment_detail.html'
    context_object_name = 'appointment'

    def test_func(self):
        appointment = self.get_object()
        user = self.request.user
        # Staff can see all, patients only their own
        if user.is_staff:
            return True
        return hasattr(user, 'patient') and appointment.patient == user.patient
