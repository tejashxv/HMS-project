from django.shortcuts import render,redirect
from patient.models import Patient
from django.contrib.auth.models import User
import uuid
from django.db import connection
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from appointments.models import Appointment
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from django.http import JsonResponse

# Create your views here.
def patient(request):
    try:
        # Get search query
        search_query = request.GET.get('search', '').strip()
        status_filter = request.GET.get('status', '')
        date_filter = request.GET.get('date_range', '')
        
        # Base queryset
        patients = Patient.objects.all()
        
        # Apply search with trigram similarity
        if search_query:
            # Simple approach: use a single queryset with all conditions
            search_conditions = Q()
            
            # Search in individual fields
            search_conditions |= Q(first_name__icontains=search_query)
            search_conditions |= Q(last_name__icontains=search_query)
            search_conditions |= Q(hospital_patient_id__icontains=search_query)
            search_conditions |= Q(phone_number__icontains=search_query)
            search_conditions |= Q(email__icontains=search_query)
            
            # Split search query for name combinations
            search_words = search_query.split()
            if len(search_words) >= 2:
                # Try first word as first name, second as last name
                search_conditions |= Q(first_name__icontains=search_words[0], last_name__icontains=search_words[1])
                # Try first word as last name, second as first name
                search_conditions |= Q(first_name__icontains=search_words[1], last_name__icontains=search_words[0])
            
            # Apply search conditions
            patients = patients.filter(search_conditions)
            
            # If no results with basic search, try broader search
            if patients.count() == 0:
                # Try partial matches with different approaches
                broader_conditions = Q()
                
                # Try each word individually
                for word in search_query.split():
                    if len(word) >= 2:
                        broader_conditions |= Q(first_name__icontains=word)
                        broader_conditions |= Q(last_name__icontains=word)
                        broader_conditions |= Q(hospital_patient_id__icontains=word)
                
                patients = Patient.objects.filter(broader_conditions).order_by('first_name', 'last_name')
        
        # Apply status filter
        if status_filter:
            patients = patients.filter(status=status_filter)
        
        # Apply date filter
        now = timezone.now()
        if date_filter == 'today':
            patients = patients.filter(registration_date__date=now.date())
        elif date_filter == 'week':
            week_start = now.date() - timezone.timedelta(days=now.weekday())
            patients = patients.filter(registration_date__date__gte=week_start)
        elif date_filter == 'month':
            patients = patients.filter(registration_date__month=now.month, registration_date__year=now.year)
        elif date_filter == 'year':
            patients = patients.filter(registration_date__year=now.year)
        
        # Order by registration date if no search query
        if not search_query:
            patients = patients.order_by('-registration_date')
        
        # Pagination
        paginator = Paginator(patients, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Statistics - Calculate from ALL patients, not filtered ones
        all_patients = Patient.objects.all()
        new_this_month = all_patients.filter(registration_date__month=now.month, registration_date__year=now.year).count()
        today = timezone.now().date()
        end_of_week = today + timezone.timedelta(days=7)
        upcoming_appointments = Appointment.objects.filter(start_time__range=[today,end_of_week]).count()
        
        statuses = ['SCHEDULED', 'CANCELLED', 'RESCHEDULED', 'PENDING']
        total_patients = all_patients.count()  # Count all patients, not just filtered ones
        
    except Exception as e:
        print(f"Error in patient view: {e}")
        return render(request, 'login_main/patients.html', {
            'error': 'An error occurred while loading patients.'
        })
    
    context = {
        'active_page': 'patients',
        'page_title': 'Patients Overview',
        'patients': patients,
        'page_obj': page_obj,
        'total_patients': total_patients,
        'new_this_month': new_this_month,
        'upcoming_appointments': upcoming_appointments,
        'search_query': search_query,
        'status_filter': status_filter,
        'date_filter': date_filter,
    }
    return render(request, 'login_main/patients.html', context)


def add_patient(request):
    if request.method == 'POST':
        try:
            # Extract data from the request
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            date_of_birth = request.POST.get('date_of_birth')
            gender = request.POST.get('gender')
            blood_group = request.POST.get('blood_group')
            registration_date = request.POST.get('registration_date')
            reason = request.POST.get('reason')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')
            address = request.POST.get('address')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_phone = request.POST.get('emergency_contact_phone')
            
            curent_domain = connection.tenant.schema_name
            hospital_id =  curent_domain.upper() + "-" + uuid.uuid4().hex[:8].upper()
            user_account = User.objects.create_user(
                username=f"{first_name.lower()}_{last_name.lower()}_{hospital_id}",
                first_name=first_name,
                last_name=last_name,
                email = email,    
            )
            
            patient = Patient.objects.create(
                hospital_patient_id=hospital_id,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                phone_number=phone_number,
                email=email,
                address=address,
                reason=reason,
                emergency_contact_name= emergency_contact_name,
                emergency_contact_phone= emergency_contact_phone,
                blood_group=blood_group,
                registration_date=registration_date,
                user_account=user_account)
            patient.save()
            # print(patient.__dict__)
            
            messages.success(request, 'Patient added successfully!')
            return render(request, 'login_main/add_patient.html', {
                'success': 'Patient added successfully!'
            })
                
        except KeyError as e:
            return render(request, 'login_main/add_patient.html', {
                'error': f'Missing field: {e}'
            })
    context = {
        'active_page': 'add_patient',
    }
    return render(request, 'login_main/add_patient.html', context)



def delete_patient(request, patient_id):
    try:
        patient = Patient.objects.get(hospital_patient_id=patient_id)
        print(patient.__dict__)
        patient.delete()
        messages.success(request, 'Patient deleted successfully!')
    except Patient.DoesNotExist:
        pass
    return redirect('/patients/')


def search_patients_ajax(request):
    """AJAX endpoint for real-time patient search"""
    query = request.GET.get('q', '').strip()
    results = []
    
    if query and len(query) >= 2:
        # Split search query into words for better name matching
        search_words = query.split()
        
        # Build search conditions
        search_conditions = Q()
        
        # Search in individual fields
        search_conditions |= Q(first_name__icontains=query)
        search_conditions |= Q(last_name__icontains=query)
        search_conditions |= Q(hospital_patient_id__icontains=query)
        search_conditions |= Q(phone_number__icontains=query)
        search_conditions |= Q(email__icontains=query)
        
        # If multiple words, search for combinations (e.g., "John Doe")
        if len(search_words) >= 2:
            for i in range(len(search_words)):
                for j in range(i+1, len(search_words)):
                    # Try first_name + last_name combinations
                    search_conditions |= Q(first_name__icontains=search_words[i], last_name__icontains=search_words[j])
                    search_conditions |= Q(first_name__icontains=search_words[j], last_name__icontains=search_words[i])
        
        # Exact matches first
        exact_matches = Patient.objects.filter(search_conditions)[:5]
        
        # Broader search for partial matches
        broader_matches = Patient.objects.filter(
            Q(first_name__icontains=query[:3]) |  # First 3 chars
            Q(last_name__icontains=query[:3]) |
            Q(hospital_patient_id__icontains=query[:3]) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        ).exclude(search_conditions).order_by('first_name', 'last_name')[:5]
        
        # Combine and format results
        all_patients = list(exact_matches) + list(broader_matches)
        
        for patient in all_patients[:10]:  # Limit to 10 results
            results.append({
                'id': patient.hospital_patient_id,
                'name': f"{patient.first_name} {patient.last_name}",
                'phone': patient.phone_number or 'N/A',
                'email': patient.email or 'N/A',
                'status': patient.status,
                'registration_date': patient.registration_date.strftime('%Y-%m-%d') if patient.registration_date else 'N/A'
            })
    
    return JsonResponse(results, safe=False)