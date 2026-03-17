from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Resource(models.Model):
    SUBJECT_SUGGESTIONS = [
        'Lecture Notes', 'Assignment', 'Previous Exam Paper',
        'Textbook / Reference', 'Project', 'Lab Report',
        'Tutorial Sheet', 'Cheat Sheet', 'Other',
    ]

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    file_upload = models.FileField(upload_to='resources/%Y/%m/')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='resources')
    subject = models.CharField(max_length=100, default='Lecture Notes')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    uploaded_at = models.DateTimeField(default=timezone.now)
    download_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def filename(self):
        return os.path.basename(self.file_upload.name)

    def is_pdf(self):
        return self.file_upload.name.lower().endswith('.pdf')

    def is_txt(self):
        return self.file_upload.name.lower().endswith('.txt')

    def file_extension(self):
        _, ext = os.path.splitext(self.file_upload.name)
        return ext.lower().lstrip('.')

    def file_size_display(self):
        try:
            size = self.file_upload.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        except Exception:
            return "Unknown"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500)
    avatar_initial_color = models.CharField(max_length=7, default='#22577A')

    def __str__(self):
        return f"Profile of {self.user.username}"

    def upload_count(self):
        return self.user.uploads.count()

    def total_downloads(self):
        return sum(r.download_count for r in self.user.uploads.all())
