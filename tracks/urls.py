"""
URL configurations for the tracks app. This module contains the URL patterns 
that map to the views for listing, creating, and viewing track details.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.TrackList.as_view(), name='track-list'),
    path('<int:pk>/', views.TrackDetail.as_view(), name='track-detail'),
]
