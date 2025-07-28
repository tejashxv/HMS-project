from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
def home_tenant(request):
    print(request.user)
    return render(request, 'login_main/dashboard.html', {})


def user_logout(request):
    logout(request)
    return redirect('http://public.127.0.0.1.nip.io:8000/')  