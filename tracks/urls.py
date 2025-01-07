from django.urls import path
from . import views

urlpatterns = [
    path('', views.TrackList.as_view(), name='track-list'),
    path('<int:pk>/', views.TrackDetail.as_view(), name='track-detail'),
]

