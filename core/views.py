from django.shortcuts import render
from accounts.models import Patient
from operations.models import Room, Appointment
from billing.models import Bill

def dashboard(request):
    """
    Main dashboard view for the hospital system.
    """
    context = {
        'total_patients': Patient.objects.count(),
        'available_rooms': Room.objects.filter(current_patient__isnull=True).count(),
        'pending_appointments': Appointment.objects.filter(status='Scheduled').count(),
        'unpaid_bills': Bill.objects.filter(is_paid=False).count(),
    }
    return render(request, 'core/dashboard.html', context)
