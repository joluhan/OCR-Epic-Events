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
    
# Definition of Contract model to store contracts associated with clients and users
class Contract(models.Model):
    # Status choices defined for the Contract model
    STATUS_CHOICES = [
        ('waiting for signature', 'Waiting for signature'),
        ('signed', 'Signed'),
        ('in progress', 'In progress'),
        ('finished', 'Finished'),
        ('terminated', 'Terminated'),
        ('cancelled', 'Cancelled'),
    ]

    # Link to a Client model instance, cascading delete
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # Link to a User model instance, nullable, optional, cascading delete
    sales_rep = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Additional fields for the Contract model
    total_amount = models.FloatField(null=False) # Total amount of the contract
    amount_remaining = models.FloatField(null=False) # Amount remaining to be paid
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="waiting for signature") # Status of the contract
    created_at = models.DateField(auto_now_add=True) # Automatically set when a new contract is created
    updated_at = models.DateField(auto_now=True) # Automatically updated whenever a contract is saved

    # Custom save method to assign sales_rep from client if not set
    def save(self, *args, **kwargs): # Custom save method to assign sales_rep from client if not set
        if not self.sales_rep: # If sales_rep is not set
            self.sales_rep = self.client.sales_rep # Assign sales_rep from client
        super().save(*args, **kwargs) # Call the save method of the parent class

    # Human-readable representation of the Contract object
    def __str__(self): 
        return f"Contract {self.id} - {self.client}" # Return the contract ID and client name
