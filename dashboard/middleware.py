from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django_tenants.utils import get_tenant

EXEMPT_URLS = [
    '/user/login/',
    '/user/register/',
    '/user/register-success/',
]

class TenantLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow public schema
        if hasattr(request, 'tenant') and request.tenant.schema_name == 'public':
            return self.get_response(request)

        # Skip exempted paths
        if any(request.path.startswith(url) for url in EXEMPT_URLS):
            return self.get_response(request)

        # If not authenticated, redirect to public login
        tenant = get_tenant(request)
        print("Tenant schema name:", tenant.schema_name)
        if not request.user.is_authenticated and tenant.schema_name != 'public':
            
            login_url = "http://public.127.0.0.1.nip.io:8000/user/login/" 
            return redirect(f'{login_url}?next={request.get_full_path()}')

        return self.get_response(request)
