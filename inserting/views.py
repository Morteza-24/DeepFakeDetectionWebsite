from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UploadVideoForm, UploadImageForm
from .models import UploadVideo, UploadImage
from .LAA.LAA_inference import LAA_video, LAA_image
from .SBI.SBI_inference import SBI_video, SBI_image
import mimetypes
from django.utils.translation import gettext_lazy as _


@login_required
def upload_view(request):
    if request.method == 'POST':
        if request.POST.get("vid"):
            vid_form = UploadVideoForm(request.POST, request.FILES)
            img_form = UploadImageForm()
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
                if vid_form.cleaned_data.get("vid_new_model"):
                    result = LAA_video(uploaded_video.file.path)
                else:
                    result = SBI_video(uploaded_video.file.path)
                uploaded_video.fakeness = result
                uploaded_video.save()
                vid_form = UploadVideoForm()
                return render(request, 'inserting/upload.html', {'vid_form': vid_form, 'img_form': img_form, 'result': f"{result}%", 'file_path': uploaded_video.file.url})
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
                if img_form.cleaned_data.get("img_new_model"):
                    result = LAA_image(uploaded_image.file.path)
                else:
                    result = SBI_image(uploaded_image.file.path)
                uploaded_image.fakeness = result
                uploaded_image.save()
                img_form = UploadImageForm()
                return render(request, 'inserting/upload.html', {'vid_form': vid_form, 'img_form': img_form, 'result': f"{result}%", 'file_path': uploaded_image.file.url, 'img': True})
    else:
        vid_form = UploadVideoForm()
        img_form = UploadImageForm()
    img = (request.method == 'POST') and (not request.POST.get("vid"))
    return render(request, 'inserting/upload.html', {'vid_form': vid_form, 'img_form': img_form, 'img': img})
