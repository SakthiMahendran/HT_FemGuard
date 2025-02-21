from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.middleware.csrf import get_token
from django.core.exceptions import ValidationError
from django.db import IntegrityError

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
    Registers a new user (Admin or Regular User).
    Expects JSON fields:
      - username (required)
      - password (required)
      - is_admin (optional, defaults to False)
      - full_name
      - date_of_birth
      - aadhar_no
      - phone_no
      - address
      - email
      - emergency_contact
      - student_or_working
      - company_school_name
      - blood_group
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))

            username = body.get('username')
            password = body.get('password')
            is_admin = body.get('is_admin', False)

            # Additional fields
            full_name = body.get('full_name')
            date_of_birth = body.get('date_of_birth')  # "YYYY-MM-DD" or any format you handle
            aadhar_no = body.get('aadhar_no')
            phone_no = body.get('phone_no')
            address = body.get('address')
            email = body.get('email')
            emergency_contact = body.get('emergency_contact')
            student_or_working = body.get('student_or_working')
            company_school_name = body.get('company_school_name')
            blood_group = body.get('blood_group')

            # Check required fields
            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)

            # Check if user already exists
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            # Create the user
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                is_admin=is_admin,
                email=email
            )

            # Update additional fields
            user.full_name = full_name
            user.aadhar_no = aadhar_no
            user.phone_no = phone_no
            user.address = address
            user.emergency_contact = emergency_contact
            user.student_or_working = student_or_working
            user.company_school_name = company_school_name
            user.blood_group = blood_group

            # For date_of_birth, you can parse or store as string. 
            # If the frontend sends "YYYY-MM-DD", do:
            if date_of_birth:
                try:
                    user.date_of_birth = date_of_birth  # If it's in proper ISO format, Django can handle it directly
                except (ValueError, ValidationError):
                    return JsonResponse({"error": "Invalid date format for date_of_birth"}, status=400)

            user.save()

            return JsonResponse({"message": "User registered successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"error": str(e)}, status=400)
    
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
        try:
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
                    "sessionid": sessionid,
                    "csrftoken": token
                }, status=200)

            return JsonResponse({"error": "Invalid admin credentials"}, status=401)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

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
        "email": request.user.email,
        "full_name": request.user.full_name,
        "date_of_birth": request.user.date_of_birth,
        "aadhar_no": request.user.aadhar_no,
        "phone_no": request.user.phone_no,
        "address": request.user.address,
        "emergency_contact": request.user.emergency_contact,
        "student_or_working": request.user.student_or_working,
        "company_school_name": request.user.company_school_name,
        "blood_group": request.user.blood_group,
        "is_admin": request.user.is_admin,
        "message": "User is authenticated"
    }, status=200)
