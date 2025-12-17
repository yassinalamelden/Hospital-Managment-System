from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from operations.models import Room

class RoomListView(ListView):
    model = Room
    template_name = 'operations/room_list.html'
    context_object_name = 'rooms'
    
    # ... (other classes remain same)

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

class RoomVacateView(View):
    def post(self, request, pk, *args, **kwargs):
        room = get_object_or_404(Room, pk=pk)

        # If already empty, just inform user
        if room.current_patient is None:
            messages.info(request, "Room is already available.")
            return redirect("room-list")

        # Vacate using model method
        room.vacate()

        messages.success(request, "Room vacated successfully.")
        return redirect("room-list")

from operations.forms import RoomAssignForm


class RoomVacateView(View):
    def post(self, request, pk, *args, **kwargs):
        room.vacate()

        messages.success(request, "Room vacated successfully.")
        return redirect("room-list")

class RoomAssignView(UpdateView):
    model = Room
    form_class = RoomAssignForm
    template_name = 'operations/room_assign.html'
    success_url = reverse_lazy('room-list')

    def form_valid(self, form):
        messages.success(self.request, f"Room assigned to {form.cleaned_data['current_patient']}.")
        return super().form_valid(form)
