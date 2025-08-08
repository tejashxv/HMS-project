from django.shortcuts import render
from django.utils import timezone
from .models import Appointment
from dashboard.models import Doctor
import datetime


# Create your views here.
def appointements(request):
    doctors = Doctor.objects.all()

    # Define the time slots for the rows
    # time_slots = [f"{hour}:00" for hour in range(7, 19)] # 7 AM to 6 PM
    time_slots = range(7, 19)

    # Get the current week's date range
    today = timezone.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    week_dates = [start_of_week + datetime.timedelta(days=i) for i in range(7)]

    # Fetch all appointments for the current week
    appointments = Appointment.objects.filter(
        start_time__date__range=[start_of_week, week_dates[-1]]
    ).select_related('doctor', 'patient')

    # Create a structured dictionary for the template
    # Format: calendar[doctor_id][date][hour] = appointment
    calendar = {doctor.user.id: {date: {} for date in week_dates} for doctor in doctors}

    for appt in appointments:
        appt_date = appt.start_time.date()
        appt_hour = appt.start_time.hour
        if appt.doctor.user.id in calendar and appt_date in calendar[appt.doctor.user.id]:
            calendar[appt.doctor.user.id][appt_date][appt_hour] = appt
    

    context = {
        'active_page': 'appointments',
        'page_title': 'Appointments',
        'doctors': doctors,
        'week_dates': week_dates,
        'time_slots': time_slots,
        'calendar': calendar,
    }
    return render(request, 'login_main/appointment.html', context)