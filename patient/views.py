from django.shortcuts import render,redirect
from patient.models import Patient
from django.contrib.auth.models import User
import uuid
from django.db import connection
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from appointments.models import Appointment

# Create your views here.
def patient(request):
    try:
        patients = Patient.objects.all().order_by('-registration_date')
        paginator = Paginator(patients, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        now = timezone.now()
        new_this_month = Patient.objects.filter(registration_date__month=now.month, registration_date__year=now.year).count()
        today = timezone.now().date()
        end_of_week = today + timezone.timedelta(days=7)
        upcoming_appointments = Appointment.objects.filter(start_time__range=[today,end_of_week]).count()
        print(f"Upcoming appointments: {upcoming_appointments}")
        statuses = ['SCHEDULED', 'CANCELLED', 'RESCHEDULED', 'PENDING']
        total_patients = Patient.objects.filter(status__in=statuses).count()
        print(f"Total patients: {total_patients}")
        
    except Patient.DoesNotExist:
        return render(request, 'login_main/patients.html', {
            'error': 'No patients found.'
        })
    context = {
        'active_page': 'patients',
        'page_title': 'Patients Overview',
        'patients': patients,
        'page_obj': page_obj,
        'total_patients': total_patients,
        'new_this_month': new_this_month,
        'upcoming_appointments': upcoming_appointments,
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