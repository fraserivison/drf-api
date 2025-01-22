"""
This module contains the URL routing for the ratings app, defining
the paths for listing and viewing individual ratings.
"""

from django.urls import path
from ratings import views

urlpatterns = [
    path('', views.RatingList.as_view(), name='rating-list'),
    path('<int:pk>/', views.RatingDetail.as_view(), name='rating-detail'),
]
