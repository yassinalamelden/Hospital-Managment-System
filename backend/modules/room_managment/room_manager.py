from .room import Room
from .bed import Bed


class RoomManager:

    def __init__(self):
        self.rooms = {}

    def add_room(self, room_id, room_type, capacity):
        room = Room(room_id, room_type, capacity)
        for i in range(capacity):
            room.add_bed(Bed(f"{room_id}-B{i+1}"))
        self.rooms[room_id] = room

    def assign_bed(self, room_id, patient_id):
        room = self.rooms[room_id]
        for bed in room.beds:
            if bed.is_avaliable:
                bed.assign(patient_id)
                return bed.bed_id
        return None
    
    def release_bed(self, room_id, bed_id):
        room = self.rooms[room_id]
        for bed in room.beds:
            if bed.bed_id == bed_id:
                bed.release()
                return True
        return False
    