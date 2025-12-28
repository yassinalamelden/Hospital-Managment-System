from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.html import strip_tags
from django.contrib.auth import authenticate
from operations.models import Appointment, Room
from accounts.models import Doctor, Patient
from accounts.forms import AppointmentForm, UserUpdateForm, PatientForm
from django.db import models
from operations.models import Appointment, Room, Review
from operations.forms import ReviewForm
from ..mixins import ProfileCompletionRequiredMixin

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

            # Profile Status Flag
            if not patient.date_of_birth or patient.gender == 'Not specified' or patient.phone == 'None':
                context['profile_incomplete'] = True

        return context

class PatientBookAppointmentView(LoginRequiredMixin, ProfileCompletionRequiredMixin, CreateView):
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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
        
        # Combine Date and Time Slot
        import datetime
        date = form.cleaned_data['date']
        time_slot = form.cleaned_data['time_slot']
        # time_slot is string "HH:MM", convert to time object
        hour, minute = map(int, time_slot.split(':'))
        time_obj = datetime.time(hour, minute)
        
        # Combine
        dt = datetime.datetime.combine(date, time_obj)
        # Make aware
        self.object.date_time = timezone.make_aware(dt)
        
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


class PatientBookRoomView(LoginRequiredMixin, ProfileCompletionRequiredMixin, View):
    def post(self, request, pk):
        if not hasattr(request.user, 'patient'):
            messages.error(request, "You must have a patient profile to book a room. Please contact administration.")
            return redirect('client-portal')
        
        room = get_object_or_404(Room, pk=pk)
        
        if room.is_occupied:
            messages.error(request, f"Room {room.room_number} is already occupied.")
            return redirect('room-availability')
        
        # Check if patient already has a room
        patient = request.user.patient
        if hasattr(patient, 'room') and patient.room:
            messages.error(request, f"You are already assigned to Room {patient.room.room_number}. Please vacate it first.")
            return redirect('room-availability')

        # Book the room
        room.current_patient = patient
        room.admission_date = timezone.now().date()
        room.save()
        
        messages.success(request, f"Room {room.room_number} has been successfully booked for you!")
        messages.warning(request, "IMPORTANT: If you do not check in within 24 hours, the room price will be charged to your balance and the reservation cancelled automatically.")
        return redirect('room-availability')

class RoomAvailabilityListView(LoginRequiredMixin, ProfileCompletionRequiredMixin, ListView):
    model = Room
    template_name = 'client/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        # Filter for available rooms or just list them all
        return Room.objects.all().order_by('room_number')

class DoctorSearchView(LoginRequiredMixin, ProfileCompletionRequiredMixin, ListView):
    model = Doctor
    template_name = 'client/doctor_search.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        from django.db.models import Avg, Count
        queryset = Doctor.objects.filter(is_active=True).annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )
        specialty = self.request.GET.get('specialty')
        name_query = self.request.GET.get('doctor') # Matches input name="doctor" from home.html
        
        if specialty:
            queryset = queryset.filter(specialty=specialty)
        
        if name_query:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(name__icontains=name_query)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Doctor.objects.values_list('specialty', flat=True).distinct().order_by('specialty')
        return context

class DoctorDetailView(LoginRequiredMixin, View):
    template_name = 'client/doctor_detail.html'

    def get(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        reviews = doctor.reviews.all().order_by('-created_at')
        form = ReviewForm()
        
        # Calculate average rating
        avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
        
        context = {
            'doctor': doctor,
            'reviews': reviews,
            'form': form,
            'avg_rating': round(avg_rating, 1),
            'star_range': range(1, 6)
        }
        return render(request, self.template_name, context)
        
    def post(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        if not hasattr(request.user, 'patient'):
             messages.error(request, "Only patients can leave reviews.")
             return redirect('doctor-detail', pk=pk)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.doctor = doctor
            review.patient = request.user.patient
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect('doctor-detail', pk=pk)
            
        reviews = doctor.reviews.all().order_by('-created_at')
        avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
        
        context = {
            'doctor': doctor,
            'reviews': reviews,
            'form': form,
            'avg_rating': round(avg_rating, 1),
            'star_range': range(1, 6)
        }
        return render(request, self.template_name, context)


class AccountSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'client/profile.html'

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
            
            # Check if profile is now complete
            patient = request.user.patient
            if patient.date_of_birth and patient.gender != 'Not specified' and patient.phone != 'None':
                messages.success(request, "Your profile is complete! You can now book appointments.")
            else:
                messages.warning(request, "Your profile has been updated, but is still incomplete. Please ensure Date of Birth, Gender, and Phone are set.")
                
            return redirect('client-portal')
        
        return render(request, self.template_name, {'u_form': u_form, 'p_form': p_form})

class AccountPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('account-settings')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        messages.success(self.request, "Your password has been changed successfully!")
        return response

class ClientReviewsView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'client/my_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        if hasattr(self.request.user, 'patient'):
            return Review.objects.filter(patient=self.request.user.patient).order_by('-created_at')
        return Review.objects.none()
