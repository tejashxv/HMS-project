from django.shortcuts import render

# Create your views here.
def patient(request):
    context = {
        'active_page': 'patients',
        'page_title': 'Patients Overview',
    }
    return render(request, 'login_main/patients.html', context)


def add_patient(request):
    context = {
        'active_page': 'add_patient',
    }
    return render(request, 'login_main/add_patient.html', context)