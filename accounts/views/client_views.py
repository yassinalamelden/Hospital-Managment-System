from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.html import strip_tags
from django.contrib.auth import authenticate
from operations.models import Appointment, Room
from accounts.models import Doctor, Patient
from accounts.forms import AppointmentForm, UserUpdateForm, PatientForm

class VerifyPasswordView(LoginRequiredMixin, View):
    template_name = 'accounts/verify_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        
        if user is not None:
            request.session['account_verified'] = True
            return redirect('account-settings')
        else:
            messages.error(request, "Incorrect password. Access denied.")
            return render(request, self.template_name)

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
            # Current data
            context['appointments'] = patient.appointments.all().order_by('-date_time')
            context['bills'] = patient.bills.all().order_by('-issued_date')
            context['patient'] = patient

            # Summary Metrics (Feature C & D)
            from django.utils import timezone
            from django.db.models import Sum
            
            # 1. Upcoming Appointments
            context['upcoming_count'] = patient.appointments.filter(
                date_time__gte=timezone.now(),
                status='Scheduled'
            ).count()

            # 2. Total Unpaid Balance
            unpaid_total = patient.bills.filter(
                payment_status__in=['PENDING', 'PARTIAL']
            ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            context['unpaid_total'] = unpaid_total

            # 3. Latest Visit
            last_visit = patient.appointments.filter(
                status='Completed'
            ).order_by('-date_time').first()
            context['last_visit'] = last_visit.date_time if last_visit else None

            # 4. Stay Status
            context['current_room'] = patient.room if hasattr(patient, 'room') else None

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

class AccountSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account_settings.html'

    def dispatch(self, request, *args, **kwargs):
        # Require password verification before accessing this view
        if not request.session.get('account_verified'):
            return redirect('verify-password')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'patient'):
            context['u_form'] = UserUpdateForm(instance=self.request.user)
            context['p_form'] = PatientForm(instance=self.request.user.patient)
        return context

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PatientForm(request.POST, instance=request.user.patient)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            
            messages.success(request, "Your account has been updated!")
            return redirect('account-settings')
        
        return render(request, self.template_name, {'u_form': u_form, 'p_form': p_form})

class AccountPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('account-settings')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        messages.success(self.request, "Your password has been changed successfully!")
        return response
