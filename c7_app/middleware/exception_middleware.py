import traceback
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        # Handle all unhandled exceptions (like DB errors, code crashes, etc.)
        return render(request, 'error.html', {
            'error_code': 500,
            'error_title': 'Internal Server Error',
            'error_message': str(exception),
        }, status=500)

    def process_response(self, request, response):
        # Handle 404 responses
        if response.status_code == 404:
            return render(request, 'error.html', {
                'error_code': 404,
                'error_title': 'Page Not Found',
                'error_message': 'The page you’re looking for doesn’t exist.',
            }, status=404)
        return response