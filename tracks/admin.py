"""
This module contains the admin configuration for the Track model,
defining how tracks are displayed and managed in the Django admin interface.
"""

from django.contrib import admin
from .models import Track

class TrackAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Track model. Allows for displaying,
    filtering, searching, and updating tracks in the admin panel.
    """
    list_display = (
        'id', 'title', 'owner', 'profile', 'genre', 
        'created_at', 'average_rating', 'ratings_count'
    )
    list_filter = ('genre', 'created_at', 'owner')
    search_fields = ('title', 'description', 'owner__username')
    ordering = ('-created_at',)
    readonly_fields = ('average_rating', 'ratings_count')

    actions = ['update_all_ratings']

    def update_all_ratings(self, request, queryset):
        """
        Action to update the average ratings for all selected tracks.
        """
        for track in queryset:
            track.update_average_rating()
        self.message_user(request, "Average ratings updated for selected tracks.")

    update_all_ratings.short_description = "Update average ratings for selected tracks"

admin.site.register(Track, TrackAdmin)
