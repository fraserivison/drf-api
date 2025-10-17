"""
Views for handling API routes for the drf_api project.

Includes routes for the root and logout functionality.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings


@api_view()
def root_route(request):
    """
    Handles the root API route.
    Returns a welcome message when accessed.
    """
    return Response({
        "message": "Welcome to my drf API!"
    })


@api_view(['POST'])
def logout_route(request):
    """
    Handles the logout route.
    Clears authentication cookies and logs out the user by setting the JWT 
    cookies to expire immediately.
    """
    response = Response({
        "message": "Successfully logged out."
    })
    response.set_cookie(
        key=settings.JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=settings.JWT_AUTH_SAMESITE,
        secure=settings.JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=settings.JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=settings.JWT_AUTH_SAMESITE,
        secure=settings.JWT_AUTH_SECURE,
    )
    return response
