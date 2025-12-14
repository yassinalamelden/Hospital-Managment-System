from django.urls import path
from .views import DoctorListView, DoctorCreateView, PatientListView, PatientCreateView

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/add/', DoctorCreateView.as_view(), name='doctor-create'),
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/add/', PatientCreateView.as_view(), name='patient-create'),
]
