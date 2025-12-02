from .schedule import Schedule
from .appointment import Appointment

appointments = []
schedules = []

def add_schedule(doctor_id, day, start_time, end_time):
    s = Schedule(doctor_id, day, start_time, end_time)
    schedules.append(s)
    return s

def is_doctor_available(doctor_id, date, time):
    for s in schedules:
        if s.doctor_id == doctor_id and s.day == date.strftime("%A"):
            if s.start_time <= time <= s.end_time:
                break
    else:
        return False

    for a in appointments:
        if a.doctor_id == doctor_id and a.date == date and a.time == time and a.status == "confirmed":
            return False

    return True

def book_appointment(appointment_id, doctor_id, patient_name, date, time):
    if not is_doctor_available(doctor_id, date, time):
        return "Doctor not available"

    a = Appointment(appointment_id, doctor_id, patient_name, date, time)
    appointments.append(a)
    return a

def cancel_appointment(appointment_id):
    for a in appointments:
        if a.appointment_id == appointment_id:
            a.cancel()
            return "Appointment canceled"
    return "Not found"

def view_doctor_appointments(doctor_id):
    return [a for a in appointments if a.doctor_id == doctor_id]
