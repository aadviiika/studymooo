from django.contrib import admin
from .models import Resource, Profile


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'notes_type', 'course_name', 'uploaded_by', 'uploaded_at', 'download_count')
    list_filter = ('notes_type', 'uploaded_at')
    search_fields = ('title', 'description', 'course_name', 'uploaded_by__username')
    readonly_fields = ('uploaded_at', 'download_count')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)