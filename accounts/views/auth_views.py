from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import AccessMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

class CustomLoginView(LoginView):
    """
    Enhanced login view with role-based redirection.
    - Admin/Staff → admin-dashboard
    - Patient → client-portal
    - No Role → home
    """
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        user = self.request.user
        
        # Priority 1: Admin/Staff users
        if user.is_staff or user.is_superuser:
            messages.success(self.request, f'Welcome back, {user.username}! (Admin)')
            return reverse_lazy('admin-dashboard')
        
        # Priority 2: Regular patients with patient profile
        if hasattr(user, 'patient'):
            messages.success(self.request, f'Welcome back, {user.username}!')
            return reverse_lazy('client-portal')
        
        # Priority 3: Users without specific role
        messages.info(self.request, f'Welcome, {user.username}! Please complete your profile.')
        return reverse_lazy('home')

class SignUpView(CreateView):
    """User registration view"""
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        from accounts.models import Patient
        Patient.objects.get_or_create(
            user=user,
            defaults={
                'name': user.username,
                'age': 0,  # Default or ask to update later
                'gender': 'Not specified',
                'phone': 'None'
            }
        )
        messages.success(self.request, 'Account created successfully! Please log in.')
        return redirect(self.success_url)

class CustomLogoutView(LogoutView):
    """Custom logout with redirect to home"""
    next_page = 'home'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, f'Goodbye, {request.user.username}!')
        return super().dispatch(request, *args, **kwargs)


# Custom Access Control Mixins
class StaffRequiredMixin(AccessMixin):
    """
    Verify that the current user is authenticated and is staff.
    Usage: Add to any view that should be staff-only.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_staff:
            messages.error(request, 'Access denied. Staff privileges required.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
