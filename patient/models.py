from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Patient(models.Model):
    """
    Represents a patient registered at a specific hospital (tenant).
    This model lives inside the tenant's schema.
    """
    hospital_patient_id = models.CharField(max_length=20, unique=True, help_text="Unique Patient ID within the hospital")

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_phone = models.CharField(max_length=15)
    
    blood_group = models.CharField(max_length=5, blank=True)    
    registration_date = models.DateTimeField(auto_now_add=True)
    
    user_account = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='patient_profile'
    )
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
        ('suspended', 'Suspended'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', help_text="Patient's current status")
    last_visit_date = models.DateField(default=None, blank=True, null=True, help_text="Date of the last visit to the hospital")
    reason = models.TextField(blank=True, null=True, help_text="Reason for the last visit or any additional notes")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.hospital_patient_id})"