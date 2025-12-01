from backend.modules.staff_management import Staff

class nurse(Staff):   
   
    def __init__(self, id, name, age, password, department, salary, shift):
        super().__init__(id, name, age, password, department, salary)
        self.shift = shift  
        self.rooms = []

    def view_dashboard(self):
        # POLYMORPHISM##
        print(f"\n=== nurse ===")
        print(f"nurse {self.name} | Shift: {self.shift}")
        print(f"Assigned Rooms: {', '.join(self.rooms)}")

    def assign_room(self, room_number):
        self.rooms.append(room_number)
        print(f"nurse {self.name} assigned to Room {room_number}.")
