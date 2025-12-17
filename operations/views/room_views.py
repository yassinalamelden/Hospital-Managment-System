from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from operations.models import Room

class RoomListView(ListView):
    model = Room
    template_name = 'operations/room_list.html'
    context_object_name = 'rooms'

class RoomCreateView(CreateView):
    model = Room
    template_name = 'operations/room_form.html'
    fields = ['room_number', 'room_type', 'price_per_night']
    success_url = reverse_lazy('room-list')
