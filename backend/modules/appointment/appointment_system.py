from datetime import datetime, timedelta
from .schedule import Schedule
from .appointment import Appointment


class AppointmentSystem:
    SLOT_DURATION = timedelta(minutes=30)
    MAX_APPOINTMENTS_PER_DAY = 10

    def __init__(self):
        self.appointments = []
        self.schedules = []


    def add_schedule(self, doctor_id, day, start_time, end_time):
        schedule = Schedule(doctor_id, day, start_time, end_time)
        self.schedules.append(schedule)
        return schedule

    def is_doctor_available(self, doctor_id, date, time):

        in_schedule = False
        for s in self.schedules:
            if s.doctor_id == doctor_id and s.day == date.strftime("%A"):
                if s.start_time <= time < s.end_time:
                    in_schedule = True
                    break

        if not in_schedule:
            return False


        daily_count = sum(
            1 for a in self.appointments
            if a.doctor_id == doctor_id
            and a.date == date
            and a.status in ["confirmed", "pending"]
        )
        if daily_count >= self.MAX_APPOINTMENTS_PER_DAY:
            return False


        for a in self.appointments:
            if (
                a.doctor_id == doctor_id
                and a.date == date
                and a.time == time
                and a.status == "confirmed"
            ):
                return False

        return True


    def book_appointment(self, appointment_id, doctor_id, patient_name, date, time):

        for a in self.appointments:
            if (
                a.patient_name == patient_name
                and a.date == date
                and a.time == time
                and a.status == "confirmed"
            ):
                return "Patient already has an appointment at this time"

        if not self.is_doctor_available(doctor_id, date, time):
            return "Doctor not available"

        appointment = Appointment(
            appointment_id,
            doctor_id,
            patient_name,
            date,
            time,
            status="confirmed"
        )
        self.appointments.append(appointment)
        return appointment


    def cancel_appointment(self, appointment_id):
        for a in self.appointments:
            if a.appointment_id == appointment_id:
                a.status = "canceled"
                return "Appointment canceled"
        return "Not found"
    def reschedule_appointment(self, appointment_id, new_date, new_time):
        for a in self.appointments:
            if a.appointment_id == appointment_id:
                if not self.is_doctor_available(a.doctor_id, new_date, new_time):
                    return "Doctor not available"
                a.date = new_date
                a.time = new_time
                a.status = "confirmed"
                return "Appointment rescheduled"
        return "Not found"


    def view_doctor_appointments(self, doctor_id):
        return [
            a for a in self.appointments
            if a.doctor_id == doctor_id
        ]

    def view_appointments_by_date(self, date):
        return [
            a for a in self.appointments
            if a.date == date
        ]
    
    def get_available_slots(self, doctor_id, date):
        slots = []

        for s in self.schedules:
            if s.doctor_id == doctor_id and s.day == date.strftime("%A"):
                current = s.start_time
                while current < s.end_time:
                    if self.is_doctor_available(doctor_id, date, current):
                        slots.append(current)
                    current = (
                        datetime.combine(date, current)
                        + self.SLOT_DURATION
                    ).time()

        return slots
