from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('register/', hospital_register, name='hospital_register'),
    path('register-success/', hospital_register_success, name='hospital_register_success'),
    path('login/',hospital_login, name='hospital_login'),
]
