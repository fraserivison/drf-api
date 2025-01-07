from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import root_route, logout_route

urlpatterns = [
    path('', root_route),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/logout/', logout_route),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    #path('auth/social/', include('allauth.socialaccount.urls')),
    #path('accounts/', include('allauth.urls')),
    
    # Include app-specific URLs
    path('profiles/', include('profiles.urls')),
    path('tracks/', include('tracks.urls')),
    path('comments/', include('comments.urls')),
    path('ratings/', include('ratings.urls')),
    path('followers/', include('followers.urls')),
    path('events/', include('events.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


