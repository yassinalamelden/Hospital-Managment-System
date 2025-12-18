from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from accounts.views.auth_views import StaffRequiredMixin
from operations.models import Appointment, Room
from accounts.models import Patient, Doctor
from billing.models import Bill
from django.db.models import Sum


class HomeView(TemplateView):
    """Public landing page"""
    template_name = 'home.html'


class AdminDashboardView(StaffRequiredMixin, TemplateView):
    """
    Main admin dashboard with statistics.
    Only accessible to staff users.
    """
    template_name = 'core/admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_patients'] = Patient.objects.count()
        context['total_doctors'] = Doctor.objects.count()
        
        context['pending_appointments'] = Appointment.objects.filter(status='Pending').count()
        context['unpaid_bills'] = Bill.objects.filter(payment_status='Unpaid').count()
        
        context['total_users'] = User.objects.count()
        context['total_rooms'] = Room.objects.count()

        context['occupied_rooms'] = Room.objects.filter(current_patient__isnull=False).count()
        
        revenue_data = Bill.objects.filter(payment_status='Paid').aggregate(Sum('total_amount'))
        context['total_revenue'] = revenue_data['total_amount__sum'] or 0

        return context


class ManageUsersView(StaffRequiredMixin, ListView):
    """
    User management view for admins.
    Lists all users with actions to promote/deactivate.
    """
    model = User
    template_name = 'admin/manage_users.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        
        # Filter by search query
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(username__icontains=search) | queryset.filter(email__icontains=search)
        
        # Filter by role
        role = self.request.GET.get('role')
        if role == 'staff':
            queryset = queryset.filter(is_staff=True)
        elif role == 'patient':
            queryset = queryset.filter(is_staff=False, is_active=True)
        elif role == 'inactive':
            queryset = queryset.filter(is_active=False)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = User.objects.count()
        context['staff_count'] = User.objects.filter(is_staff=True).count()
        context['patient_count'] = User.objects.filter(is_staff=False, is_active=True).count()
        context['inactive_count'] = User.objects.filter(is_active=False).count()
        return context


class PromoteUserView(StaffRequiredMixin, View):
    """Toggle user's staff status"""
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        # Prevent self-demotion
        if user == request.user:
            messages.error(request, 'You cannot change your own admin status.')
            return redirect('manage-users')
        
        # Toggle staff status
        user.is_staff = not user.is_staff
        user.save()
        
        action = 'promoted to' if user.is_staff else 'removed from'
        messages.success(request, f'User {user.username} has been {action} admin.')
        return redirect('manage-users')


class DeactivateUserView(StaffRequiredMixin, View):
    """Toggle user's active status"""
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        # Prevent self-deactivation
        if user == request.user:
            messages.error(request, 'You cannot deactivate your own account.')
            return redirect('manage-users')
        
        # Toggle active status
        user.is_active = not user.is_active
        user.save()
        
        action = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'User {user.username} has been {action}.')
        return redirect('manage-users')


# Review Management (Placeholder - will need Review model)
class ManageReviewsView(StaffRequiredMixin, TemplateView):
    """
    Review management view for admins.
    Note: Requires a Review model to be created.
    """
    template_name = 'admin/manage_reviews.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Placeholder - replace with actual Review model
        context['reviews'] = []
        context['total_reviews'] = 0
        context['pending_reviews'] = 0
        return context
