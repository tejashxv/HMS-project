from django.db import models
from django.contrib.auth.models import User
from django_tenants.models import TenantMixin, DomainMixin
# Create your models here.


class Hospital(TenantMixin):
    hospital_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    subdomain = models.SlugField(max_length=100, unique=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_hospital',)
    created_at = models.DateTimeField(auto_now_add=True)
    auto_create_schema = True
    def __str__(self):
        return self.hospital_name
    
    
    
class Domain(DomainMixin):
    pass