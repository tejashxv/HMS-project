from django.contrib import admin
from django.urls import path,include
from dashboard.views import home_tenant

urlpatterns = [
    path('', home_tenant, name='home_tenant'),
]
