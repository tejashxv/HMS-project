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
    today = timezone.now().date()
    end_of_week = today + timezone.timedelta(days=7)
    upcoming_appointments = Appointment.objects.select_related('patient', 'doctor__user').filter(start_time__range=[today,end_of_week])
    print(upcoming_appointments)
    upcoming_appointments_count = upcoming_appointments.count()
    
    context = {
        'active_page': 'home_tenant',
        'page_title': 'Dashboard Overview',
        'appointments': appointment,
        'upcoming_appointments': upcoming_appointments,
        'upcoming_appointments_count': upcoming_appointments_count,
    }
    return render(request, 'login_main/dashboard.html', context)


def user_logout(request):
    logout(request)
    return redirect('http://public.127.0.0.1.nip.io:8000/')  


