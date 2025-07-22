from django.shortcuts import render

# Create your views here.
def hospital_register(request):
    if request.method == 'POST':
        try:
            hospital_name = request.POST.get('hospital-name')
            hospital_address = request.POST.get('hospital-address')
            hospital_phone = request.POST.get('hospital-phone')
            hospital_subdomain = request.POST.get('subdomain')
            admin_name = request.POST.get('admin-name')
            admin_email =  request.POST.get('admin-email')
            password = request.POST.get('password')
    return render(request, 'users/hospital_registration.html')