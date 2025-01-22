"""
App configuration for the profiles app.

This file contains the configuration for the profiles app, including
the default auto field and the name of the app.
"""

from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """
    Configuration for the profiles app.

    Sets the default auto field and app name for the profiles application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'
