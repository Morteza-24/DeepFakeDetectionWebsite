from django.core.management.base import BaseCommand, CommandError
from datetime import timedelta
from django.utils import timezone
import os
from inserting.models import UploadImage, UploadVideo
from django.utils.translation import gettext_lazy as _

class Command(BaseCommand):
    help = _("حذف فایل‌هایی که بیش از 10 روز از آپلود آنها گذشته")
    
    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=10,
            help= _("مشخص کردن تعداد روزهایی که از آپلودشدن فایل‌ها گذشته و باید حذف شوند")
        )
    
    def handle(self, *args, **kwargs):
        days = kwargs['days']
        ten_days_ago = timezone.now() - timedelta(days= days)
        try:
            image_queryset= UploadImage.objects.filter(upload_date__lt= ten_days_ago)
            image_count= image_queryset.count()
            for obj in image_queryset:
                file_path = obj.file.path
                if file_path and os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        raise CommandError(f"Error deleting file {file_path}: {e}")   
                obj.delete()
                    
            video_queryset= UploadVideo.objects.filter(upload_date__lt= ten_days_ago)
            video_count= video_queryset.count()
            for obj in video_queryset:
                file_path = obj.file.path
                if file_path and os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        raise CommandError(f"Error deleting file {file_path}: {e}")
                obj.delete()
            if image_count == 0 and video_count == 0:
                self.stdout.write(self.style.SUCCESS(_("هیچ فایلی برای حذف وجود ندارد.")))
            else:
                self.stdout.write(self.style.SUCCESS(_("{} تصویر و {} ویدئو حذف گردیدند.").format(image_count, video_count)))
        
        except CommandError as e:
            self.stderr.write(self.style.ERROR(str(e)))
            raise e                  
