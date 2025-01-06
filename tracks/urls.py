from django.urls import path
from . import views

urlpatterns = [
    path('tracks/', views.TrackList.as_view(), name='track-list'),
    path('tracks/<int:pk>/', views.TrackDetail.as_view(), name='track-detail'),
]
