class Appointment:
    def __init__(self, appointment_id, doctor_id, patient_name, date, time):
        self.appointment_id = appointment_id
        self.doctor_id = doctor_id
        self.patient_name = patient_name
        self.date = date
        self.time = time
        self.status = "confirmed"

    def cancel(self):
        self.status = "canceled"

    def __str__(self):
        return f"Appointment {self.appointment_id}: {self.patient_name} — {self.date} at {self.time} ({self.status})"
