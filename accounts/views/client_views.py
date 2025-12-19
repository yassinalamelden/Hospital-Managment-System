from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from operations.models import Appointment, Room
from accounts.models import Doctor
from accounts.forms import AppointmentForm

class ClientPortalView(LoginRequiredMixin, TemplateView):
    template_name = 'client/portal.html'

    def dispatch(self, request, *args, **kwargs):
        # Redirect staff away from client portal
        if request.user.is_staff:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'patient'):
            patient = self.request.user.patient
            context['appointments'] = patient.appointments.all().order_by('-date_time')
            context['bills'] = patient.bills.all().order_by('-issued_date')
            context['patient'] = patient
        return context

class PatientBookAppointmentView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'client/book_appointment.html'
    success_url = reverse_lazy('patient-appointments')

    def get_initial(self):
        initial = super().get_initial()
        doctor_id = self.request.GET.get('doctor')
        if doctor_id:
            initial['doctor'] = doctor_id
        return initial

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'patient'):
            from django.contrib import messages
            messages.error(request, "You must have a patient profile to book an appointment. Please contact administration.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Save appointment first
        self.object = form.save(commit=False)
        self.object.patient = self.request.user.patient
        self.object.save()
        
        # Billing Logic integration
        from billing.models import Bill, BillItem
        payment_loc = form.cleaned_data.get('payment_location')
        method = 'CARD' if payment_loc == 'platform' else 'CASH'
        
        # Create the bill
        bill = Bill.objects.create(
            patient=self.request.user.patient,
            payment_method=method,
            payment_status='PENDING'
        )
        
        # Create exact bill item for transparency
        BillItem.objects.create(
            bill=bill,
            item_name=f"Consultation: Dr. {self.object.doctor.name} ({self.object.doctor.specialty})",
            unit_price=self.object.doctor.consultation_fee,
            quantity=1
        )
        
        from django.contrib import messages
        messages.success(self.request, f"Appointment successfully booked! A bill for ${self.object.doctor.consultation_fee} has been generated.")
        
        return redirect(self.get_success_url())

class PatientAppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'client/appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        if hasattr(self.request.user, 'patient'):
            return Appointment.objects.filter(patient=self.request.user.patient).order_by('-date_time')
        return Appointment.objects.none()


class RoomAvailabilityListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'client/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        # Filter for available rooms or just list them all
        return Room.objects.all().order_by('room_number')

class DoctorSearchView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'client/doctor_search.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        queryset = Doctor.objects.filter(is_active=True)
        specialty = self.request.GET.get('specialty')
        if specialty:
            queryset = queryset.filter(specialty=specialty)
        return queryset
