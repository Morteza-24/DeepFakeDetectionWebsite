from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import UploadVideoForm
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
            return JsonResponse({'message': 'ویدئو با موفقیت آپلود شد!', 'file_path': save_path})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = UploadVideoForm()
    return render(request, 'upload_video.html', {'form': form})

