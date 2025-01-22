"""
This module defines custom permissions for the application.
"""

from rest_framework import permissions


class IsownerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read-only permissions are granted for all other users.
    """
    def has_object_permission(self, request, view, obj):
        """
        Return True if the request method is safe (GET, HEAD, OPTIONS),
        or if the request user is the owner of the object.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
