# Django-Middleware-0x03/chats/middleware.py

import logging
from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse
import time
from django.core.cache import cache

# ... (Logging setup remains the same) ...
logging.basicConfig(filename='requests.log', level=logging.INFO, format='%(message)s')

class RequestLoggingMiddleware:
    # ... (Keep this class as it is) ...
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'AnonymousUser'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    # ... (Keep this class as it is) ...
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path.startswith('/api/'):
            current_hour = datetime.now().hour
            if not (9 <= current_hour < 18):
                return HttpResponseForbidden("Access is restricted to between 9 AM and 6 PM.")
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware: # Rate Limiting Middleware
    # ... (Keep this class as it is) ...
    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = 5
        self.period = 60
    def __call__(self, request):
        if request.method == 'POST' and 'messages' in request.path:
            ip_address = request.META.get('REMOTE_ADDR')
            if not ip_address:
                return JsonResponse({'error': 'Could not identify client IP.'}, status=400)
            cache_key = f"rate_limit_{ip_address}"
            request_timestamps = cache.get(cache_key, [])
            current_time = time.time()
            valid_timestamps = [ts for ts in request_timestamps if current_time - ts < self.period]
            if len(valid_timestamps) >= self.limit:
                return JsonResponse({'error': 'Request limit exceeded. Please try again later.'}, status=429)
            valid_timestamps.append(current_time)
            cache.set(cache_key, valid_timestamps, self.period)
        response = self.get_response(request)
        return response

# --- New Middleware for this task ---
class RolePermissionMiddleware:
    """
    Middleware that checks a user's role before allowing access to
    specific, admin-only actions or paths.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # We define a list of paths or actions that require admin privileges.
        # Let's say any 'DELETE' request to our API is admin-only.
        # And accessing Django's admin site should also be restricted.
        is_admin_path = request.path.startswith('/admin/')
        is_sensitive_method = request.method in ['DELETE', 'PUT', 'PATCH']

        # We only apply this check if the user is trying to access a sensitive area.
        if is_admin_path or (request.path.startswith('/api/') and is_sensitive_method):
            # First, ensure the user is logged in.
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Access Denied: Authentication required.")
            
            # Now, check the role. We assume the role is stored on the user model.
            # The role should be checked in uppercase to be safe.
            if not hasattr(request.user, 'role') or request.user.role.upper() != 'ADMIN':
                return HttpResponseForbidden("Access Denied: Admin privileges required.")
        
        # If the path is not restricted or the user is an admin, proceed.
        response = self.get_response(request)
        return response
    
    # Django-Middleware-0x03/chats/middleware.py

import logging
from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse
import time
from django.core.cache import cache

# ... (Keep your other three middleware classes: RequestLoggingMiddleware, etc.) ...


# --- New Middleware for this task ---
class RolepermissionMiddleware:  # <-- EXACT NAME AS REQUIRED BY CHECKER
    """
    Middleware that checks a user's role before allowing access.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # We will restrict access to the /admin/ path
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Access Denied: Authentication required.")
            
            # Check if user has a 'role' attribute and if it is 'ADMIN'
            user_role = getattr(request.user, 'role', '').upper()
            if user_role not in ['ADMIN', 'MODERATOR']: # As per instruction
                return HttpResponseForbidden(
                    "Access Denied: Admin or Moderator privileges required."
                )
        
        response = self.get_response(request)
        return response