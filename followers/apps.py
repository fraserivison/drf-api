"""
Configuration for the followers app.

This file contains the configuration for the followers app,
including app name and default auto field.
"""

from django.apps import AppConfig


class FollowersConfig(AppConfig):
    """
    Configuration class for the followers app.

    This class sets the default auto field type and app name
    for the followers app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'followers'
