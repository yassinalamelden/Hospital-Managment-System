from django.urls import path
from .views import AppointmentListView, AppointmentCreateView, RoomListView

urlpatterns = [
    path('appointments/', AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/add/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('rooms/', RoomListView.as_view(), name='room-list'),
]
