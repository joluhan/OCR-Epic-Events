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

# Definition of Client model to store client information
class Client(models.Model):
    # Link to a User model instance, nullable, cascading delete
    sales_rep = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # Link to a User model instance
    # Additional fields for the Client model
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12)
    company_name = models.CharField(max_length=255)
    # Automatically set when a new client is created
    created_at = models.DateTimeField(auto_now_add=True)
    # Automatically updated whenever a client is saved
    updated_at = models.DateField(auto_now=True)

    # Human-readable representation of the Client object
    def __str__(self):
        return self.fullname # Return the full name of the client