from django.shortcuts import render
from django.utils import timezone
from .models import Appointment
from dashboard.models import Doctor
import datetime


# Create your views here.
def appointements(request):
    doctors = Doctor.objects.all()
    time_slots = range(7, 19)

    # Get the current week's date range
    today = timezone.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    week_dates = [start_of_week + datetime.timedelta(days=i) for i in range(7)]

    # Fetch all appointments for the current week
    appointments = Appointment.STATUS_CHOICES
    print(appointments)
    
    app = Appointment.objects.all()
    print(app)
    
    

    context = {
        'active_page': 'appointments',
        'page_title': 'Appointments',
        'doctors': doctors,
        'week_dates': week_dates,
        'time_slots': time_slots,
        'appointments': appointments,
        'patient' : app
    }
    return render(request, 'login_main/appointment.html', context)