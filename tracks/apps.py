"""
This module contains the configuration for the Tracks app in the Django project.
It defines the configuration class for the app, including the default auto field type.
"""

from django.apps import AppConfig


class TracksConfig(AppConfig):
    """
    Configuration class for the Tracks app. Sets the default auto field type
    and the name of the app within the Django project.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracks'
