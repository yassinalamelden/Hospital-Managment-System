class Schedule:
    def __init__(self, doctor_id, day, start_time, end_time):
        self.doctor_id = doctor_id
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"{self.day} — {self.start_time} to {self.end_time}"