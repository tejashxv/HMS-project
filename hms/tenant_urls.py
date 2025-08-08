from django.contrib import admin
from django.urls import path,include
from dashboard.views import *
from patient.views import *
from appointments.views import *

urlpatterns = [
    path('', home_tenant, name='Dashboard'),
    path('logout/', user_logout, name='user_logout'),
    path('appointments/', appointements, name='Appointments'),
    path('patients/', patient, name='Patients'),
]
