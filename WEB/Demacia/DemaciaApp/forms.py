from django import forms
from .models import VideoFile
class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoFile
        fields = {'user_id','upload_file',}

# class AdminForm(forms.ModelForm):
#     class Meta:
#         model = Admin
#         fields = ['admin_id','admin_password','name']

