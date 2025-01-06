from django.urls import path
from ratings import views

urlpatterns = [
    path('ratings/', views.RatingList.as_view(), name='rating-list'),
    path('ratings/<int:pk>/', views.RatingDetail.as_view(), name='rating-detail'),
]
