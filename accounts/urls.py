from django.urls import path
from .views import (
    DoctorListView, DoctorCreateView, 
    PatientListView, PatientCreateView, PatientDashboardView
)
from .views.auth_views import CustomLoginView, SignUpView, CustomLogoutView
from .views.client_views import (
    ClientPortalView, PatientBookAppointmentView, 
    RoomAvailabilityListView, DoctorSearchView,
    PatientAppointmentListView
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
    path('find-doctor/', DoctorSearchView.as_view(), name='doctor-search'),

    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/add/', DoctorCreateView.as_view(), name='doctor-create'),
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/add/', PatientCreateView.as_view(), name='patient-create'),
    path('patients/<int:pk>/dashboard/', PatientDashboardView.as_view(), name='patient-dashboard'),
]
