from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class BaseUserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('نام خود را وارد کنید'),
        }),
        label=_('نام')
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('نام خانوادگی خود را وارد کنید'),
        }),
        label=_('نام خانوادگی')
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('ایمیل خود را وارد کنید'),
        }),
        label=_('ایمیل')
    )
    phone_number = forms.CharField(
        max_length=11,
        required=True,
        validators=[RegexValidator(
            regex=r'^09\d{9}$',
            message=_('شماره تلفن باید با 09 شروع شود و 11 رقمی باشد.')  
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('شماره تلفن خود را وارد کنید'),
            'dir': 'ltr'
        }),
        label=_('شماره تلفن')
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number']


class SignUpForm(UserCreationForm, BaseUserForm):
    class Meta(BaseUserForm.Meta):
        model = CustomUser
        fields = [
            'first_name', 'last_name',
            'email', 'phone_number',
            'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['email'].widget.attrs.update({'autofocus': False})
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('رمز عبور خود را وارد کنید'),
            'dir': 'ltr'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('رمز عبور خود را مجددا وارد کنید'),
            'dir': 'ltr'
        })

        self.fields['password1'].label = _('رمز عبور')
        self.fields['password2'].label = _('تکرار رمز عبور')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _('این ایمیل قبلاً توسط کاربر دیگری استفاده شده است.')
            )

        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        User = get_user_model()

        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(
                _('این شماره تلفن قبلاً توسط کاربر دیگری استفاده شده است.')
            )

        return phone_number


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('ایمیل خود را وارد کنید'),
            'dir': 'ltr'
        }),
        label=_('ایمیل')
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('رمز عبور خود را وارد کنید'),
            'dir': 'ltr'
        }),
        label=_('رمز عبور')
    )


class UserUpdateForm(BaseUserForm):
    class Meta(BaseUserForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        existing_users = CustomUser.objects.exclude(pk=self.instance.pk).filter(phone_number=phone_number)
        if existing_users.exists():
            raise forms.ValidationError(
                _('این شماره تلفن قبلاً توسط کاربر دیگری استفاده شده است.')
            )
        return phone_number
    

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('ایمیل خود را وارد کنید'),
            'dir': 'ltr'
        }),
        label=_('ایمیل')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('رمز عبور جدید خود را وارد کنید'),
            'dir': 'ltr'
        }),
        label=_('رمز عبور جدید')
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('رمز عبور جدید خود را مجددا وارد کنید'),
            'dir': 'ltr'
        }),
        label=_('تکرار رمز عبور جدید')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""