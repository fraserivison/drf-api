"""
Configuration for the events app.

This file defines the configuration class for the events app.
"""

from django.apps import AppConfig


class EventsConfig(AppConfig):
    """
    Configuration for the events app.

    This class is used to configure the 'events' app in Django.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'
