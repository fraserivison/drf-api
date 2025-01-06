from django.urls import path
from followers import views

urlpatterns = [
    path('followers/', views.FollowerList.as_view(), name='follower-list'),
    path('followers/<int:pk>/', views.FollowerDetail.as_view(), name='follower-detail'),
]
