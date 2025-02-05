from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import UploadVideoForm, UploadImageForm
from .models import UploadVideo, UploadImage
from .ai.media_inference import infer_video, infer_image
import mimetypes
from django.utils.translation import gettext_lazy as _

@login_required
def upload_image_view(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['file']
            file_type, _ = mimetypes.guess_type(image_file.name)
            if not file_type or not file_type.startswith('image'):
                return JsonResponse({'error': 'فرمت تصویر معتبر نمی‌باشد.'}, status= 400)
            
            uploaded_image = UploadImage( 
                title = form.cleaned_data['title'], 
                file = image_file, 
                uploader = request.user
            )
            
            uploaded_image.save()
            result = infer_image(uploaded_image.file.path)
            form = UploadVideoForm()
            return render(request, 'inserting/upload.html', {'form': form, 'result': result, 'file_path': uploaded_image.file.url})
        
    else:
        form = UploadImageForm()
    return render(request, 'inserting/upload.html', {'form': form})

@login_required
def upload_video_view(request):
    if request.method == 'POST':
        form = UploadVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = form.cleaned_data['file']
            file_type, _ = mimetypes.guess_type(video_file.name)
            if not file_type or not file_type.startswith('video'):
                return JsonResponse({'error': 'فرمت ویدئو معتبر نمی‌باشد.'}, status= 400)

            uploaded_video = UploadVideo( 
                title = form.cleaned_data['title'], 
                file = video_file, 
                uploader = request.user
            )

            uploaded_video.save()
            result = infer_video(uploaded_video.file.path)
            form = UploadVideoForm()
            return render(request, 'inserting/upload.html', {'form': form, 'result': result, 'file_path': uploaded_video.file.url})
        
    else:
        form = UploadVideoForm()
    return render(request, 'inserting/upload.html', {'form': form})

