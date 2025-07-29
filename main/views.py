from django.shortcuts import render
from django.db import connection
from django_tenants.utils import get_tenant 
from hms.settings import INSTALLED_APPS


# Create your views here.
def home(request):
    print(request.user)
    return render(request, 'main/home.html', {})


