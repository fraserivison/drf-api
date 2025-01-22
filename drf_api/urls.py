"""
URL configuration for the drf_api project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from profiles.views import CustomLoginView
from .views import root_route, logout_route

urlpatterns = [
    # Root route
    path('', root_route),

    # Admin and authentication endpoints
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # JWT token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # dj-rest-auth and registration
    path('dj-rest-auth/login/', CustomLoginView.as_view(), name='custom-login'),
    path('dj-rest-auth/logout/', logout_route),
    #path('dj-rest-auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    # Social auth and profiles
    path('auth/social/', include('allauth.socialaccount.urls')),
    path('accounts/', include('allauth.urls')),
    path('profiles/', include('profiles.urls')),

    # Other app endpoints
    path('tracks/', include('tracks.urls')),
    path('comments/', include('comments.urls')),
    path('ratings/', include('ratings.urls')),
    path('followers/', include('followers.urls')),
    path('events/', include('events.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
