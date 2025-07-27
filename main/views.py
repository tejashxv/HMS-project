from django.shortcuts import render
from django.db import connection
from django_tenants.utils import get_tenant 
from hms.settings import INSTALLED_APPS
# Create your views here.
def home(request):
    tenant = get_tenant(request)
    print("INSTALLED_APPS:", INSTALLED_APPS)
    print("CURRENT TENANT:", tenant)
    print("CURRENT SCHEMA:", connection.schema_name)
    return render(request, 'main/home.html', {})