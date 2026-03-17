from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Resource, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class ResourceUploadForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file_upload', 'course_name', 'notes_type']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Data Structures Final Notes'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Briefly describe this resource…'
            }),
            'course_name': forms.TextInput(attrs={
                'placeholder': 'e.g. Data Structures, Calculus II, Organic Chemistry…'
            }),
            'notes_type': forms.Select(),
        }
        labels = {
            'course_name': 'Course Name',
            'notes_type': 'Notes Type',
        }

    def clean_file_upload(self):
        file = self.cleaned_data.get('file_upload')
        if file:
            allowed_exts = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.txt', '.zip', '.png', '.jpg', '.jpeg']
            ext = '.' + file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''
            if ext not in allowed_exts:
                raise forms.ValidationError(f"File type '{ext}' is not allowed.")
            if file.size > 50 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 50MB.")
        return file


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell other students about yourself…'}),
        }