from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
from .forms import UploadVideoForm, UploadImageForm
from .models import UploadVideo, UploadImage
from .ai.media_inference import infer_video, infer_image
import mimetypes
from django.utils.translation import gettext_lazy as _

@login_required
def upload_view(request):
    if request.method == 'POST':
        if request.GET.get("img") == None:
            vid_form = UploadVideoForm(request.POST, request.FILES)
            img_form = UploadVideoForm()
            if vid_form.is_valid():
                video_file = vid_form.cleaned_data['file']
                file_type, _ = mimetypes.guess_type(video_file.name)
                if not file_type or not file_type.startswith('video'):
                    vid_form.add_error("file", _("فرمت ویدئو معتبر نمی‌باشد."))
                    return render(request, 'inserting/upload.html', {'vid_form': vid_form, 'img_form': img_form})
                uploaded_video = UploadVideo(
                    title = vid_form.cleaned_data['title'],
                    file = video_file,
                    uploader = request.user
                )
                uploaded_video.save()
                result = infer_video(uploaded_video.file.path)
                vid_form = UploadVideoForm()
                return render(request, 'inserting/upload.html', {'vid_form': vid_form, 'img_form': img_form, 'result': result, 'file_path': uploaded_video.file.url})
        else:
            img_form = UploadImageForm(request.POST, request.FILES)
            vid_form = UploadVideoForm()
            if img_form.is_valid():
                image_file = img_form.cleaned_data['file']
                file_type, _ = mimetypes.guess_type(image_file.name)
                if not file_type or not file_type.startswith('image'):
                    img_form.add_error("file", _("فرمت تصویر معتبر نمی‌باشد."))
                    return render(request, 'inserting/upload.html', {'vid_form': vid_form, 'img_form': img_form, 'img': True})
                uploaded_image = UploadImage(
                    title = img_form.cleaned_data['title'],
                    file = image_file,
                    uploader = request.user
                )
                uploaded_image.save()
                result = infer_image(uploaded_image.file.path)
                img_form = UploadVideoForm()
                return render(request, 'inserting/upload.html', {'vid_form': vid_form, 'img_form': img_form, 'result': result, 'file_path': uploaded_image.file.url, 'img': True})
    else:
        vid_form = UploadVideoForm()
        img_form = UploadImageForm()
    return render(request, 'inserting/upload.html', {'vid_form': vid_form, 'img_form': img_form, 'img': request.GET.get("img") != None})
