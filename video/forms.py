from django import forms
import mimetypes
from django.utils.translation import gettext_lazy as _

class UploadVideoForm(forms.Form):
    title = forms.CharField(max_length=50, required=True, label=_('عنوان ویدئو'))
    title.widget.attrs.update({"class": "form-control", "placeholder": _("placeholder")})
    file = forms.FileField(required=True, label=_('فایل ویدئو'))
    file.widget.attrs.update({"class": "form-control"})

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file:
            file_type, _ = mimetypes.guess_type(file.name)
            if not file_type or not file_type.startswith('video'):
                raise forms.ValidationError(_('فایل آپلودشده معتبر نمی‌باشد.'))
        return file
