from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventList.as_view(), name='event-list'),
    path('<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
]