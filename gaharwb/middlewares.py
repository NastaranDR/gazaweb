from django.http import HttpResponseForbidden
from django.conf import settings

class RestrictAdminIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            allowed_ips = getattr(settings, 'ALLOWED_ADMIN_IPS', [])
            ip = request.META.get('REMOTE_ADDR')

            if ip not in allowed_ips:
                return HttpResponseForbidden("دسترسی غیرمجاز")

        return self.get_response(request)
