"""
Admin configurations for the profiles app.

This file registers the Profile model with the Django admin site.
"""

from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
