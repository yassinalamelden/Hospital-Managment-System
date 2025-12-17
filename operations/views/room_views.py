from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
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

class RoomUpdateView(UpdateView):
    model = Room
    template_name = 'operations/room_form.html'
    fields = ['room_number', 'room_type', 'price_per_night']
    success_url = reverse_lazy('room-list')

class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'operations/room_confirm_delete.html'
    success_url = reverse_lazy("room-list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Prevent deleting occupied rooms
        if self.object.current_patient is not None:
            messages.error(request,"Cannot delete an occupied room. Vacate it first.")
            return redirect(self.success_url)

        messages.success(request, "Room deleted successfully.")
        return super().post(request, *args, **kwargs)
