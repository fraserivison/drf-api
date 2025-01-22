"""
URLs for the followers app.

This file maps URL paths to views for managing follower relationships, including listing 
followers and viewing follower details.
"""

from django.urls import path
from followers import views
from . import views

urlpatterns = [
    path('', views.FollowerList.as_view(), name='follower-list'),
    path('<int:pk>/', views.FollowerDetail.as_view(), name='follower-detail'),
]
