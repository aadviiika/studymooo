from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import FileResponse, Http404
from django.db.models import Q
import os

from .models import Resource, Course, Profile
from .forms import RegisterForm, ResourceUploadForm, ProfileEditForm


def get_or_create_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


def home(request):
    query = request.GET.get('q', '').strip()
    course_filter = request.GET.get('course', '')
    subject_filter = request.GET.get('subject', '').strip()

    resources = Resource.objects.select_related('course', 'uploaded_by').all()

    if query:
        resources = resources.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(subject__icontains=query) |
            Q(course__name__icontains=query) |
            Q(course__code__icontains=query)
        )
    if course_filter:
        resources = resources.filter(course__id=course_filter)
    if subject_filter:
        resources = resources.filter(subject__icontains=subject_filter)

    trending = Resource.objects.order_by('-download_count')[:5]
    recent = resources[:12]
    courses = Course.objects.all()

    return render(request, 'home.html', {
        'resources': recent,
        'trending': trending,
        'courses': courses,
        'query': query,
        'course_filter': course_filter,
        'subject_filter': subject_filter,
        'total_count': resources.count(),
    })


def resource_detail(request, pk):
    resource = get_object_or_404(Resource.objects.select_related('course', 'uploaded_by'), pk=pk)
    related = Resource.objects.filter(
        Q(course=resource.course) | Q(subject__icontains=resource.subject)
    ).exclude(pk=pk)[:4]

    notes_preview = None
    if resource.is_txt():
        try:
            with open(resource.file_upload.path, 'r', encoding='utf-8', errors='replace') as f:
                notes_preview = f.read(8000)
        except Exception:
            pass

    return render(request, 'resource_detail.html', {
        'resource': resource,
        'related': related,
        'notes_preview': notes_preview,
    })


def download_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if not resource.file_upload:
        raise Http404("File not found.")
    Resource.objects.filter(pk=pk).update(download_count=resource.download_count + 1)
    file_path = resource.file_upload.path
    if not os.path.exists(file_path):
        raise Http404("File not found on server.")
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{resource.filename()}"'
    return response


@login_required
def upload_resource(request):
    if request.method == 'POST':
        form = ResourceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            messages.success(request, f'"{resource.title}" uploaded successfully!')
            return redirect('resource_detail', pk=resource.pk)
    else:
        form = ResourceUploadForm()
    return render(request, 'upload_resource.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            get_or_create_profile(user)
            login(request, user)
            messages.success(request, f'Welcome to StudyMoo, {user.username}!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            get_or_create_profile(user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_or_create_profile(user)
    uploads = Resource.objects.filter(uploaded_by=user).select_related('course').order_by('-uploaded_at')
    return render(request, 'profile.html', {
        'profile_user': user,
        'profile': profile,
        'uploads': uploads,
    })


@login_required
def edit_profile(request):
    profile = get_or_create_profile(request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def delete_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        title = resource.title
        if resource.file_upload and os.path.exists(resource.file_upload.path):
            os.remove(resource.file_upload.path)
        resource.delete()
        messages.success(request, f'"{title}" has been deleted.')
        return redirect('profile', username=request.user.username)
    return render(request, 'confirm_delete.html', {'resource': resource})
