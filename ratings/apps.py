"""
Configuration for the ratings app.

This module contains the app configuration for the ratings app, which handles
the rating functionality for tracks or other objects.
"""

from django.apps import AppConfig


class LikesConfig(AppConfig):
    """
    Configuration for the ratings app.

    This class defines the configuration for the ratings app, including the 
    default auto field and the app name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ratings'
