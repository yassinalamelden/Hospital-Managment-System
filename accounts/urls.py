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
    PatientBookRoomView
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    
    path('my-portal/', ClientPortalView.as_view(), name='client-portal'),
    path('my-appointments/', PatientAppointmentListView.as_view(), name='patient-appointments'),
    path('dashboard/', PatientListView.as_view(), name='dashboard'),  # Admin Dashboard alias

    # Client Actions
    path('book-appointment/', PatientBookAppointmentView.as_view(), name='book-appointment'),
    path('find-room/', RoomAvailabilityListView.as_view(), name='room-availability'),
    path('rooms/<int:pk>/book/', PatientBookRoomView.as_view(), name='book-room'),
    path('find-doctor/', DoctorSearchView.as_view(), name='doctor-search'),
    path('account/verify/', VerifyPasswordView.as_view(), name='verify-password'),
    path('account/settings/', AccountSettingsView.as_view(), name='account-settings'),
    path('account/password/', AccountPasswordChangeView.as_view(), name='password-change'),

    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/add/', DoctorCreateView.as_view(), name='doctor-create'),
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/add/', PatientCreateView.as_view(), name='patient-create'),
    path('patients/<int:pk>/dashboard/', PatientDashboardView.as_view(), name='patient-dashboard'),
]
