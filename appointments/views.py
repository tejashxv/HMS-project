from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .models import Appointment
from patient.models import Patient
from dashboard.models import Doctor
import datetime
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Value, CharField
from django.contrib.postgres.search import TrigramSimilarity
from django.urls import reverse




# Create your views here.
def appointements(request):
    doctors = Doctor.objects.select_related('user').all()
    print(f"Found {doctors.count()} doctors:")
    for doctor in doctors:
        print(f"Doctor PK: {doctor.pk}, Name: {doctor.user.first_name} {doctor.user.last_name}, Specialization: {doctor.specialization}")
    time_slots = range(7, 19)

    # Get the current week's date range
    today = timezone.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    week_dates = [start_of_week + datetime.timedelta(days=i) for i in range(7)]

    # Fetch all appointments for the current week
    appointments = Appointment.STATUS_CHOICES
    app = Appointment.objects.all()
    
    # Get today's appointments
    todays_appointments = Appointment.objects.filter(
        start_time__date=today
    ).select_related('patient', 'doctor__user').order_by('start_time')
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        print(f"Received doctor ID: {doctor_id}")
        # doctor = get_object_or_404(Doctor, user_id=doctor_id)
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        status = request.POST.get('status')
        reason_for_visit = request.POST.get('reason_for_visit')
        
        print(f"Form data received:")
        print(f"Patient ID: {patient_id}")
        print(f"Doctor ID: {doctor_id}")
        print(f"Start Time: {start_time}")
        print(f"End Time: {end_time}")
        print(f"Status: {status}")
        print(f"Reason: {reason_for_visit}")
        
        # Validate required fields
        if not patient_id:
            print("Error: No patient selected")
        if not doctor_id:
            print("Error: No doctor selected")
        if not start_time:
            print("Error: No start time provide")
        if not end_time:
            print("Error: No end time provided")
            
        # Get the actual objects and create appointment
        if patient_id and doctor_id and start_time and end_time:
            try:
                patient = get_object_or_404(Patient, hospital_patient_id=patient_id)
                doctor = get_object_or_404(Doctor, pk=doctor_id)
                
                print(f"Patient found: {patient.first_name} {patient.last_name}")
                print(f"Doctor found: Dr. {doctor.user.first_name} {doctor.user.last_name}")
                
                # Parse and make timezone-aware datetime objects
                start_datetime = parse_datetime(start_time)
                end_datetime = parse_datetime(end_time)
                
                if start_datetime and timezone.is_naive(start_datetime):
                    start_datetime = timezone.make_aware(start_datetime)
                if end_datetime and timezone.is_naive(end_datetime):
                    end_datetime = timezone.make_aware(end_datetime)
                
                # Create the appointment
                appointment = Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    start_time=start_datetime,
                    end_time=end_datetime,
                    status=status or 'scheduled',
                    reason_for_visit=reason_for_visit or ''
                )
                
                messages.success(request, f'Appointment booked successfully for {patient.first_name} {patient.last_name} with Dr. {doctor.user.first_name} {doctor.user.last_name}')
                return redirect('Appointments')
                
            except Exception as e:
                print(f"Error creating appointment: {str(e)}")
                messages.error(request, f"Error creating appointment: {str(e)}")
        else:
            messages.error(request, "Please fill in all required fields")

    context = {
        'active_page': 'appointments',
        'page_title': 'Appointments',
        'doctors': doctors,
        'week_dates': week_dates,
        'time_slots': time_slots,
        'appointments': appointments,
        'patient': app,
        'todays_appointments': todays_appointments
    }
    return render(request, 'login_main/appointment.html', context)


def search_patients(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        # Exact matches first
        exact_matches = Patient.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(hospital_patient_id__icontains=query)
        ).values(
            "hospital_patient_id", "first_name", "last_name", "phone_number"
        )

        # Fuzzy matches with trigram
        fuzzy_matches = (
            Patient.objects.annotate(
                sim_first=TrigramSimilarity("first_name", query),
                sim_last=TrigramSimilarity("last_name", query),
                sim_id=TrigramSimilarity("hospital_patient_id", query),
            )
            .filter(
                Q(sim_first__gt=0.3) |
                Q(sim_last__gt=0.3) |
                Q(sim_id__gt=0.3)
            )
            .exclude(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(hospital_patient_id__icontains=query)
            )
            .order_by("-sim_first", "-sim_last", "-sim_id")
            .values(
                "hospital_patient_id", "first_name", "last_name", "phone_number"
            )
        )

        # Merge & limit results
        results = list(exact_matches) + list(fuzzy_matches)
        results = results[:10]  # Limit for performance

    return JsonResponse(results, safe=False)



def quick_patient_lookup(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        # Exact matches first
        exact_matches = Patient.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(hospital_patient_id__icontains=query)
        ).values(
            "hospital_patient_id", "first_name", "last_name", "phone_number"
        )

        # Fuzzy matches
        fuzzy_matches = (
            Patient.objects.annotate(
                sim_first=TrigramSimilarity("first_name", query),
                sim_last=TrigramSimilarity("last_name", query),
                sim_id=TrigramSimilarity("hospital_patient_id", query),
            )
            .filter(
                Q(sim_first__gt=0.3) |
                Q(sim_last__gt=0.3) |
                Q(sim_id__gt=0.3)
            )
            .exclude(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(hospital_patient_id__icontains=query)
            )
            .order_by("-sim_first", "-sim_last", "-sim_id")
            .values(
                "hospital_patient_id", "first_name", "last_name", "phone_number"
            )
        )

        merged = list(exact_matches) + list(fuzzy_matches)

        # Add profile URL (if patient detail view exists)
        results = []
        for patient in merged[:10]:
            try:
                profile_url = reverse("patient_detail", kwargs={"patient_id": patient["hospital_patient_id"]})
            except:
                # If patient_detail URL doesn't exist, use patients page or None
                profile_url = reverse("Patients") if "Patients" else None
            
            results.append({
                **patient,
                "profile_url": profile_url
            })

    return JsonResponse(results, safe=False)