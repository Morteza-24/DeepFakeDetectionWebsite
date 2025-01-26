from django.contrib import admin
from .models import UploadVideo

class UploadVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'upload_date')   
    list_filter = ('upload_date', 'uploader') 
    search_fields = ('title', 'uploader__username')  
    ordering = ('-upload_date',)  

    fieldsets = (
    (None, {
        'fields': ('title', 'file', 'uploader')
    }),
    ('اطلاعات تاریخ', {
        'fields': ('upload_date',),
        'classes': ('collapse',),
    }),
)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploader = request.user
        super().save_model(request, obj, form, change)

admin.site.register(UploadVideo, UploadVideoAdmin)
