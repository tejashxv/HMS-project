from django.utils import timezone
from appointments.models import Appointment

def global_context(request):
    """
    Context processor to add global data to all templates
    """
    context = {}
    
    try:
        # Get current time
        now = timezone.now()
        
        # Today's appointments count
        todays_appointments_count = Appointment.objects.filter(
            start_time__date=now.date()
        ).count()
        
        # Today's remaining appointments count
        todays_remaining_count = Appointment.objects.filter(
            start_time__gte=now,
            start_time__date=now.date()
        ).count()
        
        # This week's appointments count
        week_start = now.date() - timezone.timedelta(days=now.weekday())
        week_end = week_start + timezone.timedelta(days=6)
        week_appointments_count = Appointment.objects.filter(
            start_time__date__range=[week_start, week_end]
        ).count()
        
        # Patient counts
        from patient.models import Patient
        
        # New patients this month
        new_patients_this_month = Patient.objects.filter(
            registration_date__month=now.month,
            registration_date__year=now.year
        ).count()
        
        # New patients today
        new_patients_today = Patient.objects.filter(
            registration_date__date=now.date()
        ).count()
        
        context.update({
            'todays_appointments_count': todays_appointments_count,
            'todays_remaining_count': todays_remaining_count,
            'week_appointments_count': week_appointments_count,
            'new_patients_this_month': new_patients_this_month,
            'new_patients_today': new_patients_today,
        })
        
    except Exception as e:
        # If there's any error (like database not available), provide defaults
        context.update({
            'todays_appointments_count': 0,
            'todays_remaining_count': 0,
            'week_appointments_count': 0,
            'new_patients_this_month': 0,
            'new_patients_today': 0,
        })
    
    return context