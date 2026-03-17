from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resource/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('resource/<int:pk>/download/', views.download_resource, name='download_resource'),
    path('resource/<int:pk>/delete/', views.delete_resource, name='delete_resource'),
    path('upload/', views.upload_resource, name='upload_resource'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # edit_profile MUST be before profile/<username>/ to avoid conflict
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
]