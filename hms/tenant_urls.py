from django.contrib import admin
from django.urls import path,include
from dashboard.views import *
from patient.views import *
from appointments.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_tenant, name='Dashboard'),
    path('logout/', user_logout, name='user_logout'),
    path('appointments/', appointements, name='Appointments'),
    path('patients/', patient, name='Patients'),
    path('add_patient/', add_patient, name='AddPatient'),
]
