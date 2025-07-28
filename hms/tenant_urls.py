from django.contrib import admin
from django.urls import path,include
from dashboard.views import *

urlpatterns = [
    path('', home_tenant, name='home_tenant'),
    path('logout/', user_logout, name='user_logout'),
]
