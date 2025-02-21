from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Extend Django's AbstractUser to add custom fields.
    'AbstractUser' already includes fields like username, email, first_name, last_name, password, etc.
    """
    is_admin = models.BooleanField(default=False)  # True for admin, False for users

    # Additional fields:
    full_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    aadhar_no = models.CharField(max_length=20, blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)

    # For "student/working", we can use choices or just a simple char field
    STUDENT_OR_WORKING_CHOICES = [
        ('student', 'Student'),
        ('working', 'Working'),
    ]
    student_or_working = models.CharField(
        max_length=10,
        choices=STUDENT_OR_WORKING_CHOICES,
        blank=True,
        null=True
    )
    company_school_name = models.CharField(max_length=255, blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)

    # Many-to-many fields to override default from AbstractUser
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True
    )

    def __str__(self):
        return self.username
