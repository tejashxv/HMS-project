from django.shortcuts import render
from django.utils import timezone
from .models import Appointment
from patient.models import Patient
from dashboard.models import Doctor
import datetime
# from django.contrib.postgres.search import SearchVector
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from django.urls import reverse



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
    app = Appointment.objects.all()
    
    if request.method == 'POST':
        patient = request.POST.get('patient')
        print(patient)

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
        ).annotate(
            profile_url=models.Value('', output_field=models.CharField())  # placeholder
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

        # Add profile URL
        results = [
            {
                **patient,
                "profile_url": reverse("patient_detail", kwargs={"patient_id": patient["hospital_patient_id"]})
            }
            for patient in merged[:10]
        ]

    return JsonResponse(results, safe=False)