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
    path('delete_patient/<str:patient_id>/', delete_patient, name='DeletePatient'),
    path('search-patients-ajax/', search_patients_ajax, name='search_patients_ajax'),
    path("search-patients/", search_patients, name="search_patients"),
    path('quick-patient-search/', quick_patient_lookup, name='quick_patient_search'),
    path('user/', include('users.urls')),  # Add users URLs to tenant context
]
