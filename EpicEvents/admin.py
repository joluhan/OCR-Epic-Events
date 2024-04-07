from django.contrib import admin  # Import the admin module from Django's built-in 'contrib' package.

# Import the specific models from the 'epicevents.models' module that you want to manage through the admin interface.
from EpicEvents.models import Client, Contract, Event, User

# This is a comment that explains the purpose of the code block below, which is to register models.

# The following lines register models with the admin site. 
# This makes the models available in the Django admin interface, allowing to create, update, and delete entries for these models.

admin.site.register(User)      # Register the User model with the admin site.
admin.site.register(Client)    # Register the Client model with the admin site.
admin.site.register(Contract)  # Register the Contract model with the admin site.
admin.site.register(Event)     # Register the Event model with the admin site.
