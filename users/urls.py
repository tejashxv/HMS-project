from django.urls import path,include
from .views import *
from main.views import home  # or your dashboard view

app_name = 'users'

urlpatterns = [
    path('register/', hospital_register, name='hospital_register'),
    path('register-success/', hospital_register_success, name='hospital_register_success'),
    path('login/',hospital_login, name='hospital_login'),
]
