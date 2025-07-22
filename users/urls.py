from django.contrib import admin
from django.urls import path,include
from .views import hospital_register

urlpatterns = [
    path('register/', hospital_register, name='hospital_register'),
]
