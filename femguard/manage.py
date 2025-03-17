#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django

def ensure_admin_user():
    """Ensure that at least one admin user exists in the database."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'femguard.settings')
    
    try:
        django.setup()  # Set up Django
        from authentication.models import CustomUser  # Import the CustomUser model
        
        # Check if an admin user exists
        if not CustomUser.objects.filter(is_admin=True).exists():
            print("No admin found. Creating default admin user...")
            admin_user = CustomUser.objects.create_superuser(username="admin", password="adminpass", is_admin=True)
            admin_user.save()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists. Proceeding...")
    
    except Exception as e:
        print(f"Error ensuring admin user: {e}")
        sys.exit(1)

def main():
    """Run administrative tasks."""
    ensure_admin_user()  # Ensure an admin user exists before proceeding
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'femguard.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
