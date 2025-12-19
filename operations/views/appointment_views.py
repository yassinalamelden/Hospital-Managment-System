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

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Billing Logic integration (Feature C)
        from billing.models import Bill, BillItem
        payment_loc = form.cleaned_data.get('payment_location')
        method = 'CARD' if payment_loc == 'platform' else 'CASH'
        
        # Create the bill for the selected patient
        bill = Bill.objects.create(
            patient=self.object.patient,
            payment_method=method,
            payment_status='PENDING'
        )
        
        # Create bill item for consultation
        BillItem.objects.create(
            bill=bill,
            item_name=f"Consultation: Dr. {self.object.doctor.name} ({self.object.doctor.specialty})",
            unit_price=self.object.doctor.consultation_fee,
            quantity=1
        )
        
        from django.contrib import messages
        messages.success(self.request, f"Appointment booked and bill for ${bill.total_amount} generated.")
        
        return response

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
