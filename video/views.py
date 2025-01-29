from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import UploadVideoForm
from .ai.video_inference import infer_video
import os

@login_required
def upload_video_view(request):
    if request.method == 'POST':
        form = UploadVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = form.cleaned_data['file']
            allowed_extensions = ['mp4', 'avi', 'mov']
            file_extension = video_file.name.split('.')[-1].lower()
            
            if file_extension not in allowed_extensions:
                return JsonResponse({'error': 'فرمت فایل معتبر نمی‌باشد. فرمت‌های مجاز: mp4, avi, mov.'}, status=400)

            save_path = os.path.join('media/videos', video_file.name)
            with open(save_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)
            result = infer_video(video_file)
            form = UploadVideoForm()
            return render(request, 'video/demo.html', {'form': form, 'result': result, 'file_path': save_path})
    else:
        form = UploadVideoForm()
    return render(request, 'video/demo.html', {'form': form})
