from django.http import Http404


class AdminAccessMiddleware:
    """
    Middleware to restrict admin access to superusers only.
    Non-superusers accessing /admin/ will receive a 404 response.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated or not request.user.is_superuser:
                raise Http404('Page not found')
        
        response = self.get_response(request)
        return response
