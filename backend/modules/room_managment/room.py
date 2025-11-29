class Room:
    '''
    For Rooms Data
    '''
    def __init__(self, room_id, room_type, capacity):
        self.room_id = room_id
        self.room_type = room_type
        self.capacity = capacity
        self.beds = []

    def add_bed(self, bed):
        return self.beds.append(bed)

    def avalibale_bed(self):
        return [b for b in self.beds if b.is_available]
