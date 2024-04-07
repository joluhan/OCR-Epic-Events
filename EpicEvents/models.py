# Importing necessary classes from django.db and django.contrib.auth.models
from django.db import models # Importing models from django.db
from django.contrib.auth.models import AbstractUser # Importing AbstractUser from django.contrib.auth.models

# Definition of custom User model, extending AbstractUser to include additional fields
class User(AbstractUser):
    # Role choices defined for the User model
    ROLE_CHOICES = [
        ('sales', 'Sales'),
        ('support', 'Support'),
        ('management', 'Management'),
    ]

    # Specifies the field used as the unique identifier for login
    USERNAME_FIELD = 'username'
    # Additional fields for the User model
    fullname = models.CharField(max_length=255, unique=True) # Full name of the user
    username = models.CharField(max_length=150, unique=True) # Username of the user
    role = models.CharField(max_length=20, choices=ROLE_CHOICES) # Role of the user

    # Human-readable representation of the User object
    def __str__(self):
        return self.username # Return the username of the user
