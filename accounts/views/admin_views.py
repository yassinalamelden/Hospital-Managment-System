from django.views.generic import ListView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages 
from operations.models import Review
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Q

# --- View 1: Manage Users ---
@method_decorator(staff_member_required, name='dispatch')
class ManageUsersView(ListView):
    """
    Custom Dashboard View for Admins to manage users.
    Replaces the default Django Admin user list.
    """
    model = User
    template_name = 'admin/manage_users.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search')
        role = self.request.GET.get('role')
        queryset = User.objects.all().order_by('-date_joined')
        
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
            
        if role:
            if role == 'staff':
                queryset = queryset.filter(is_staff=True)
            elif role == 'patient':
                queryset = queryset.filter(patient__isnull=False)
            elif role == 'inactive':
                queryset = queryset.filter(is_active=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = User.objects.count()
        context['staff_count'] = User.objects.filter(is_staff=True).count()
        context['patient_count'] = User.objects.filter(patient__isnull=False).count()
        context['inactive_count'] = User.objects.filter(is_active=False).count()
        return context

# --- View 2: Manage Reviews ---
@method_decorator(staff_member_required, name='dispatch')
class ManageReviewsView(ListView):
    model = Review
    template_name = 'admin/manage_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.all().order_by('-created_at')

# --- View 3: Deactivate User (Action View) ---
@method_decorator(staff_member_required, name='dispatch')
class DeactivateUserView(View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        
        if user.is_superuser:
            messages.error(request, "Cannot deactivate a Superuser account!")
        else:
            if user.is_active:
                user.is_active = False
                messages.warning(request, f"User {user.username} has been deactivated.")
            else:
                user.is_active = True
                messages.success(request, f"User {user.username} has been reactivated.")
            
            user.save()
            
        return redirect('manage_users')

# --- View 4: Promote/Demote User ---
@method_decorator(staff_member_required, name='dispatch')
class PromoteUserView(View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        
        if user == request.user:
            messages.error(request, "You cannot change your own role.")
            return redirect('manage_users')

        if user.is_staff:
            user.is_staff = False
            # Also remove superuser status if they have it
            if user.is_superuser:
                user.is_superuser = False
            user.save()
            messages.warning(request, f"User {user.username} has been removed from Staff.")
        else:
            user.is_staff = True
            user.save()
            messages.success(request, f"User {user.username} has been promoted to Staff (Admin).")
        
        return redirect('manage_users')

# --- View 5: Delete User (Permanent) ---
@method_decorator(staff_member_required, name='dispatch')
class DeleteUserView(View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        
        if user == request.user:
            messages.error(request, "You cannot delete your own account.")
            return redirect('manage_users')
            
        username = user.username
        user.delete()
        messages.success(request, f"User {username} has been permanently deleted.")
        return redirect('manage_users')