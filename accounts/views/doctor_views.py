from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.models import Doctor
from accounts.forms import DoctorForm

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class DoctorCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'accounts/doctor_form.html'
    success_url = reverse_lazy('doctor-list')

class DoctorListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Doctor
    template_name = 'accounts/doctor_list.html'
    context_object_name = 'doctors'
