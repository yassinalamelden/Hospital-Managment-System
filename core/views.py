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
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
import base64
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend


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
        
        # Basic Counts
        context['total_patients'] = Patient.objects.count()
        context['total_doctors'] = Doctor.objects.count()
        context['pending_appointments'] = Appointment.objects.filter(status='Scheduled').count() # Renamed to Scheduled to match model status
        context['unpaid_bills'] = Bill.objects.filter(payment_status='PENDING').count()
        context['total_users'] = User.objects.count()
        context['total_rooms'] = Room.objects.count()
        context['occupied_rooms'] = Room.objects.filter(current_patient__isnull=False).count()
        
        # Revenue
        revenue_data = Bill.objects.filter(payment_status='PAID').aggregate(Sum('total_amount'))
        context['total_revenue'] = revenue_data['total_amount__sum'] or 0

        # Gender Distribution for Chart
        gender_data = Patient.objects.values('gender').annotate(count=Count('gender'))
        context['gender_labels'] = [item['gender'] for item in gender_data]
        context['gender_counts'] = [item['count'] for item in gender_data]

        # Appointment Status for Chart
        appointment_status_data = Appointment.objects.values('status').annotate(count=Count('status'))
        context['appointment_labels'] = [item['status'] for item in appointment_status_data]
        context['appointment_counts'] = [item['count'] for item in appointment_status_data]

        # Recent Activity
        context['recent_appointments'] = Appointment.objects.select_related('doctor', 'patient').order_by('-date_time')[:5]
        context['recent_bills'] = Bill.objects.select_related('patient').order_by('-issued_date')[:5]
        context['recent_patients'] = Patient.objects.order_by('-created_at')[:5]

        # Monthly Revenue (Last 6 months)
        six_months_ago = timezone.now().date().replace(day=1) - timedelta(days=150)
        monthly_revenue = Bill.objects.filter(
            payment_status='PAID', 
            issued_date__gte=six_months_ago
        ).values('issued_date__month').annotate(total=Sum('total_amount')).order_by('issued_date__month')
        
        # Mapper for month names
        import calendar
        monthly_labels = [calendar.month_name[item['issued_date__month']] for item in monthly_revenue]
        monthly_data = [float(item['total']) for item in monthly_revenue]

        # Generate Matplotlib Charts
        context['gender_chart'] = self.generate_gender_chart(
            [item['gender'] for item in gender_data],
            [item['count'] for item in gender_data]
        )
        context['status_chart'] = self.generate_status_chart(
            [item['status'] for item in appointment_status_data],
            [item['count'] for item in appointment_status_data]
        )
        context['revenue_chart'] = self.generate_revenue_chart(
            monthly_labels,
            monthly_data
        )

        return context

    def generate_chart_base64(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        string = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return f"data:image/png;base64,{string}"

    def generate_gender_chart(self, labels, counts):
        if not labels: return None
        fig, ax = plt.subplots(figsize=(4, 4))
        colors = ['#6f42c1', '#007bff', '#e83e8c', '#fd7e14']
        ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors[:len(labels)])
        ax.axis('equal')
        return self.generate_chart_base64(fig)

    def generate_status_chart(self, labels, counts):
        if not labels: return None
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(labels, counts, color='#0dcaf0')
        ax.set_title('Appointment Status')
        return self.generate_chart_base64(fig)

    def generate_revenue_chart(self, labels, data):
        if not labels: return None
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(labels, data, marker='o', color='#198754', linewidth=2)
        ax.fill_between(labels, data, color='#198754', alpha=0.1)
        ax.set_title('Monthly Revenue')
        return self.generate_chart_base64(fig)


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
