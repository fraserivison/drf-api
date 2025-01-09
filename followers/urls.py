from django.urls import path
from followers import views
from followers.views import FollowerList, FollowerDetail

urlpatterns = [
    path('', views.FollowerList.as_view(), name='follower-list'),
    path('<int:pk>/', views.FollowerDetail.as_view(), name='follower-detail'),
]

