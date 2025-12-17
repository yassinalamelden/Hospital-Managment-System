from django.urls import path
from .views import AppointmentListView, AppointmentCreateView, RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView, RoomVacateView

urlpatterns = [
    path('appointments/', AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/add/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/add/', RoomCreateView.as_view(), name='room-create'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room-update'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room-delete'),
    path("rooms/<int:pk>/vacate/", RoomVacateView.as_view(), name="room-vacate"),
]
