from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.middleware.csrf import get_token

@csrf_exempt
def get_csrf_token(request):
    """
    GET /auth/csrf_token/
    Returns a CSRF token for frontend authentication.
    """
    return JsonResponse({"csrf_token": get_token(request)})

@csrf_exempt
def user_register(request):
    """
    POST /auth/register
    Registers a new user (Admin or Regular User)
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            username = body.get('username')
            password = body.get('password')
            is_admin = body.get('is_admin', False)

            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = CustomUser.objects.create_user(username=username, password=password, is_admin=is_admin)
            return JsonResponse({"message": "User registered successfully"}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def user_login(request):
    """
    POST /auth/user_login
    Authenticates a normal user and returns a session-based login
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            username = body.get('username')
            password = body.get('password')

            user = authenticate(username=username, password=password)
            if user and not user.is_admin:
                login(request, user)
                return JsonResponse({"message": "User login successful", "is_admin": False}, status=200)
            return JsonResponse({"error": "Invalid user credentials"}, status=401)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def admin_login(request):
    """
    POST /auth/admin_login
    Returns JSON with sessionid & csrftoken if valid admin.
    """
    if request.method == 'POST':
        import json
        from django.middleware.csrf import get_token
        body = json.loads(request.body.decode('utf-8'))
        username = body.get('username')
        password = body.get('password')

        user = authenticate(username=username, password=password)
        if user and user.is_admin:
            # Log user in to create a session
            login(request, user)

            # Manually get the session key
            sessionid = request.session.session_key  # e.g. 'abcd1234'

            # Also get a csrf token
            token = get_token(request)

            return JsonResponse({
                "message": "Admin login successful",
                "is_admin": True,
                "sessionid": sessionid,    # We must supply sessionid ourselves
                "csrftoken": token         # We must supply CSRFTOKEN ourselves
            }, status=200)

        return JsonResponse({"error": "Invalid admin credentials"}, status=401)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
@login_required
def user_logout(request):
    """
    GET/POST /auth/logout
    Logs out the user
    """
    if request.method in ['GET', 'POST']:
        logout(request)
        return JsonResponse({"message": "Logout successful"}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@login_required
def get_current_user(request):
    """
    GET /auth/me
    Returns the currently logged-in user's details.
    If user is not logged in, returns 401 unauthorized (no redirect).
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=401)

    return JsonResponse({
        "username": request.user.username,
        "is_admin": request.user.is_admin,
        "message": "User is authenticated"
    }, status=200)
