from django.shortcuts import render

# Create your views here.
def home_tenant(request):
    return render(request, 'login_main/dashboard.html', {})

