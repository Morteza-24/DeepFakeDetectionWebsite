from django.db import models
from django.conf import settings
import os
from datetime import datetime
from django.utils.translation import gettext_lazy as _

def image_upload_path(instance, filename):
    return os.path.join(f'images/{instance.uploader.id}/{datetime.now().strftime("%Y/%m/%d")}', filename)

class UploadImage(models.Model):
    title = models.CharField(max_length= 50, verbose_name= 'عنوان تصویر')
    file = models.ImageField(upload_to= 'images/', verbose_name= 'فایل تصویر')
    fakeness = models.IntegerField(default=-1)
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name= 'uploaded_images',
        verbose_name= 'آپلودکننده',
    )
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ آپلود')  

    def __str__(self):
        return self.title

def video_upload_path(instance, filename):
    return os.path.join(f'videos/{instance.uploader.id}/{datetime.now().strftime("%Y/%m/%d")}', filename)

class UploadVideo(models.Model):
    title = models.CharField(max_length= 50, verbose_name= 'عنوان ویدئو')
    file = models.FileField(upload_to= 'videos/', verbose_name= 'فایل ویدئو')
    fakeness = models.IntegerField(default=-1)
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name='uploaded_videos', 
        verbose_name='آپلودکننده'
    )
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ آپلود')

    def __str__(self):
        return self.title