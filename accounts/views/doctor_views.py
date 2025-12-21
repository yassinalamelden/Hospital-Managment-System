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

from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib import messages

class ToggleDoctorStatusView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        # Prevent disabling the last active doctor if validation logic existed, 
        # but for now just toggle.
        doctor.is_active = not doctor.is_active
        doctor.save()
        status_msg = "activated" if doctor.is_active else "deactivated"
        messages.success(request, f"Doctor {doctor.name} has been {status_msg}.")
        return redirect('doctor-list')
