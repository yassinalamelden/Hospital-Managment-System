from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
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
