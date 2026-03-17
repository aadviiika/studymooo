from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os


class Resource(models.Model):
    NOTES_TYPE_CHOICES = [
        ('Lecture Notes', 'Lecture Notes'),
        ('Textbook', 'Textbook'),
        ('Question Bank', 'Question Bank'),
        ('Sample Paper', 'Sample Paper'),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    file_upload = models.FileField(upload_to='resources/%Y/%m/')
    course_name = models.CharField(max_length=200, blank=True, default='')
    notes_type = models.CharField(max_length=50, choices=NOTES_TYPE_CHOICES, default='Lecture Notes')
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

    def __str__(self):
        return f"Profile of {self.user.username}"

    def total_downloads(self):
        return sum(r.download_count for r in self.user.uploads.all())