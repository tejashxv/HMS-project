from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.db import transaction

def hospital_register(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                hospital_name = request.POST.get('hospital-name')
                hospital_address = request.POST.get('hospital-address')
                hospital_phone = request.POST.get('hospital-phone')
                hospital_subdomain = request.POST.get('subdomain').lower().strip()
                first_name = request.POST.get('first-name')
                last_name = request.POST.get('last-name')
                admin_email = request.POST.get('admin-email').lower().strip()
                password = request.POST.get('password')

                if User.objects.filter(username=admin_email).exists():
                    messages.error(request, 'User with this email already exists.')
                    return redirect('hospital_register')

                user = User.objects.create_user(
                    username=admin_email,
                    first_name=first_name,
                    last_name=last_name,
                    email=admin_email,
                    password=password
                )

                hospital = Hospital.objects.create(
                    schema_name=hospital_subdomain, 
                    hospital_name=hospital_name,
                    address=hospital_address,
                    phone_number=hospital_phone,
                    subdomain=hospital_subdomain,
                    owner=user
                )

                Domain.objects.create(
                    domain=f'{hospital_subdomain}.localhost',  # works locally
                    tenant=hospital,
                    is_primary=True
                )

                messages.success(request, 'Hospital registered successfully!')
                return redirect('hospital_register_success')

        except Exception as e:
            messages.error(request, f'Error registering hospital: {str(e)}')
            return redirect('hospital_register')

    return render(request, 'users/hospital_registration.html')


def hospital_register_success(request):
    hospital = Hospital.objects.last()  # Get the last registered hospital
    if not hospital:
        messages.error(request, 'No hospital found.')
        return redirect('hospital_register')
    messages.success(request, f'Hospital {hospital.hospital_name} registered successfully!')
    context = {
        'hospital': hospital
    }
    return render(request, 'users/hospital_registration_success.html', context)



def hospital_login(request):
    if request.method == 'POST':
        subdomain = request.POST.get('subdomain')
        password = request.POST.get('password')
        print(subdomain, password)
        try:
            hospital = Hospital.objects.get(schema_name=subdomain)
            print(hospital)
            user = hospital.owner
            if user.check_password(password):
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect(f'http://{hospital.schema_name}.localhost:8000/')  
            else:
                messages.error(request, 'Invalid password.')
        except Hospital.DoesNotExist:
            messages.error(request, 'Hospital with this subdomain does not exist.')
    
    return render(request, 'users/hospital_login.html')