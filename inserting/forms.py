from django import forms
import mimetypes
from django.utils.translation import gettext_lazy as _

class UploadImageForm(forms.Form):
    title = forms.CharField(max_length=50, required=True, label='عنوان تصویر')
    title.widget.attrs.update({"class": "form-control", "placeholder": _('عنوان تصویر را وارد کنید')})
    file = forms.FileField(required=True, label='فایل تصویر')
    file.widget.attrs.update({"class": "form-control"})

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            file_type = mimetypes.guess_type(file.name)[0]
            if not file_type or not file_type.startswith('image'):
                raise forms.ValidationError(_('فایل آپلودشده معتبر نمی‌باشد.'))
        return file

class UploadVideoForm(forms.Form):
    title = forms.CharField(max_length=50, required=True, label='عنوان ویدئو')
    title.widget.attrs.update({"class": "form-control", "placeholder": _('عنوان ویدئو را وارد کنید')})
    file = forms.FileField(required=True, label='فایل ویدئو')
    file.widget.attrs.update({"class": "form-control"})

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            file_type = mimetypes.guess_type(file.name)[0]
            if not file_type or not file_type.startswith('video'):
                raise forms.ValidationError(_('فایل آپلودشده معتبر نمی‌باشد.'))
        return file
