from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from appointments.models import *
from django.utils import timezone

# Create your views here.
def home_tenant(request):
    appointment = Appointment.objects.filter(start_time__gte=timezone.now()).order_by('start_time')[:10]
    context = {
        'active_page': 'home_tenant',
        'page_title': 'Dashboard Overview',
        'appointments': appointment,
    }
    return render(request, 'login_main/dashboard.html', context)


def user_logout(request):
    logout(request)
    return redirect('http://public.127.0.0.1.nip.io:8000/')  


