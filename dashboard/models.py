
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Doctor(models.Model):
    """
    Represents a doctor who is a staff member of a specific hospital (tenant).
    This model lives inside the tenant's schema.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True, 
        related_name='doctor_profile'
    )
    
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    
    phone_number = models.CharField(max_length=15, blank=True)
    
    bio = models.TextField(blank=True, help_text="A short biography of the doctor.")
    profile_picture = models.ImageField(upload_to='images/doctor_profiles/', null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


# ---------------------------------------------------------------------------


class Staff(models.Model):
    """
    Represents a staff member of a specific hospital (tenant).
    This model lives inside the tenant's schema.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True, # Makes the link to User the primary key
        related_name='staff_profile'
    )
    
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    
    phone_number = models.CharField(max_length=15, blank=True)
    
    bio = models.TextField(blank=True, help_text="A short biography of the staff member.")
    profile_picture = models.ImageField(upload_to='images/staff_profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.position}"
    
    
    
    
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  
    
    def __str__(self):
        return f"{self.user.username} - {self.message[:30]}"