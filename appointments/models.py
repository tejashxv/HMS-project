
from django.db import models
from django.conf import settings
from dashboard.models import Doctor
from patient.models import Patient

class Appointment(models.Model):
    """
    Represents a scheduled appointment between a patient and a doctor.
    This model lives inside the tenant's schema.
    """
    
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SCHEDULED')
    
    reason_for_visit = models.TextField(help_text="The primary reason for the appointment.")
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        help_text="The staff member who booked the appointment."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.patient} with {self.doctor} at {self.start_time.strftime('%Y-%m-%d %H:%M')}"

# ---------------------------------------------------------------------------


class MedicalRecord(models.Model):
    """
    Represents the clinical notes and records for a specific patient visit.
    This model also lives inside the tenant's schema.
    """
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='medical_records'
    )
    appointment = models.OneToOneField(
        Appointment, 
        on_delete=models.CASCADE, 
        related_name='medical_record'
    )
    
    diagnosis = models.TextField()
    prescription = models.TextField(blank=True)
    doctor_notes = models.TextField(blank=True, help_text="Internal notes from the doctor.")
    
    recorded_by = models.ForeignKey(
        Doctor, 
        on_delete=models.SET_NULL, 
        null=True
    )
    record_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record for {self.patient} on {self.record_date.strftime('%Y-%m-%d')}"

