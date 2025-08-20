from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from appointments.models import *
from django.utils import timezone

# Create your views here.
def home_tenant(request):
    appointment = Appointment.objects.select_related('patient', 'doctor__user').filter(start_time__gte=timezone.now()).order_by('start_time')[:10]
    
    # Get current time
    now = timezone.now()
    
    # Get appointments for the next 24 hours from now
    next_24_hours = now + timezone.timedelta(hours=24)
    
    upcoming_appointments = Appointment.objects.select_related('patient', 'doctor__user').filter(
        start_time__gte=now,  # From current time
        start_time__lt=next_24_hours  # Until 24 hours from now
    ).order_by('start_time')
    
    upcoming_appointments_count = upcoming_appointments.count()
    
    # Set appropriate title based on time range
    if upcoming_appointments_count > 0:
        # Check if all appointments are today
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        today_appointments = upcoming_appointments.filter(start_time__lte=today_end)
        
        if today_appointments.count() == upcoming_appointments_count:
            appointment_type = "Today's remaining"
        else:
            appointment_type = "Next 24 hours"
    else:
        # Fallback: show today's completed appointments if no upcoming ones
        today_all_appointments = Appointment.objects.select_related('patient', 'doctor__user').filter(
            start_time__date=now.date()
        ).order_by('start_time')
        
        if today_all_appointments.count() > 0:
            upcoming_appointments = today_all_appointments
            upcoming_appointments_count = today_all_appointments.count()
            appointment_type = "Today's (completed)"
        else:
            # Last resort: show recent appointments
            upcoming_appointments = Appointment.objects.select_related('patient', 'doctor__user').order_by('-start_time')[:5]
            upcoming_appointments_count = upcoming_appointments.count()
            appointment_type = "Recent"
    
    context = {
        'active_page': 'home_tenant',
        'page_title': 'Dashboard Overview',
        'appointments': appointment,
        'upcoming_appointments': upcoming_appointments,
        'upcoming_appointments_count': upcoming_appointments_count,
        'appointment_type': appointment_type,
    }
    return render(request, 'login_main/dashboard.html', context)


def user_logout(request):
    logout(request)
    return redirect('http://public.127.0.0.1.nip.io:8000/')  


