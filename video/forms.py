from django import forms
import mimetypes

class UploadVideoForm(forms.Form):
    title = forms.CharField(max_length=50, required=True, label='عنوان ویدئو')
    file = forms.FileField(required=True, label='فایل ویدئو')

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file:
            file_type, _ = mimetypes.guess_type(file.name)
            if not file_type or not file_type.startswith('video'):
                raise forms.ValidationError('فایل آپلودشده معتبر نمی‌باشد.')
        return file
