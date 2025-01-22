"""
URLs for the events app.

This file contains the URL patterns for the events, mapping each endpoint to its corresponding view.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventList.as_view(), name='event-list'),
    path('<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
]
