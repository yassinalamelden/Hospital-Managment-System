from django.views.generic import ListView
from operations.models import Room

class RoomListView(ListView):
    model = Room
    template_name = 'operations/room_list.html'
    context_object_name = 'rooms'
