from django.shortcuts import render

# Create your views here.
def patient(request):
    context = {
        'active_page': 'patients',
        'page_title': 'Patients Overview',
    }
    return render(request, 'login_main/patients.html', context)
