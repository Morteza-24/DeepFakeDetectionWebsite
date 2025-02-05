from django.urls import path
from .views import upload_video_view, upload_image_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('video/', upload_video_view, name='upload_video'),
    path('image/', upload_image_view, name='upload_image'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)