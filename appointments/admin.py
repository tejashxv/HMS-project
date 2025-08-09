from django.contrib import admin
from .models import Appointment, MedicalRecord
# Register your models here.

admin.site.register(Appointment)
admin.site.register(MedicalRecord)
