from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from accounts.models import Doctor
from accounts.forms import DoctorForm

class DoctorCreateView(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'accounts/doctor_form.html'
    success_url = reverse_lazy('doctor-list')

class DoctorListView(ListView):
    model = Doctor
    template_name = 'accounts/doctor_list.html'
    context_object_name = 'doctors'
