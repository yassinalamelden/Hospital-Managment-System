from django.urls import path
from .views import (
    DoctorListView, DoctorCreateView, 
    PatientListView, PatientCreateView, PatientDashboardView
)
from .views.auth_views import CustomLoginView, SignUpView, CustomLogoutView
from .views.client_views import (
    ClientPortalView, PatientBookAppointmentView, 
    RoomAvailabilityListView, DoctorSearchView,
    PatientAppointmentListView, AccountSettingsView, 
    AccountPasswordChangeView, VerifyPasswordView,
    PatientBookRoomView, DoctorDetailView,
    ClientReviewsView
)
from .views.admin_views import ManageUsersView, ManageReviewsView, DeactivateUserView, PromoteUserView, DeleteUserView
from .views.doctor_views import ToggleDoctorStatusView
from core.views import AdminDashboardView

urlpatterns = [
    # --- Authentication ---
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('register/', SignUpView.as_view(), name='register'),  # Alias for signup
    
    # --- Client / Patient Portal (المريض) ---
    path('my-portal/', ClientPortalView.as_view(), name='client-portal'),
    path('my-appointments/', PatientAppointmentListView.as_view(), name='patient-appointments'),
    path('portal/booking/', PatientBookAppointmentView.as_view(), name='book-appointment'),
    path('portal/reviews/', ClientReviewsView.as_view(), name='client-reviews'),
    
    # Client Features (Search & Booking)
    path('find-room/', RoomAvailabilityListView.as_view(), name='room-availability'),
    path('rooms/<int:pk>/book/', PatientBookRoomView.as_view(), name='book-room'),
    
    # Doctor Search & Profile (Client Side)
    path('find-doctor/', DoctorSearchView.as_view(), name='doctor-search'), 
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),

    # --- Account Settings ---
    path('account/verify/', VerifyPasswordView.as_view(), name='verify-password'),
    path('account/settings/', AccountSettingsView.as_view(), name='account-settings'),
    path('account/password/', AccountPasswordChangeView.as_view(), name='password-change'),

    # --- Admin Dashboard (لوحة تحكم الإدارة) ---
    path('dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'), # الرابط الرئيسي للداشبورد
    path('dashboard/users/', ManageUsersView.as_view(), name='manage_users'), # رابط إدارة المستخدمين

    path('dashboard/doctors/', DoctorListView.as_view(), name='doctor-list'), # قائمة الأطباء للإدارة
    path('dashboard/doctors/add/', DoctorCreateView.as_view(), name='doctor-create'),
    
    path('dashboard/patients/', PatientListView.as_view(), name='patient-list'),
    path('dashboard/patients/add/', PatientCreateView.as_view(), name='patient-create'),
    path('dashboard/patients/<int:pk>/', PatientDashboardView.as_view(), name='patient-dashboard'),
    path('dashboard/reviews/', ManageReviewsView.as_view(), name='manage_reviews'),
    path('dashboard/users/<int:pk>/deactivate/', DeactivateUserView.as_view(), name='deactivate_user'),
    path('dashboard/users/<int:pk>/promote/', PromoteUserView.as_view(), name='promote_user'),
    path('dashboard/users/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),
    path('dashboard/doctors/<int:pk>/toggle-status/', ToggleDoctorStatusView.as_view(), name='toggle-doctor-status'), # Doctor Toggle
]