from django.contrib import admin
from .models import Course, Resource, Profile

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('name', 'code')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'course', 'uploaded_by', 'uploaded_at', 'download_count')
    list_filter = ('subject', 'course', 'uploaded_at')
    search_fields = ('title', 'description', 'uploaded_by__username')
    readonly_fields = ('uploaded_at', 'download_count')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)
