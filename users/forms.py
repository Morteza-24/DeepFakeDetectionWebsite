from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from .models import CustomUser

class BaseUserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='نام'
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='نام خانوادگی'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='ایمیل'
    )
    phone_number = forms.CharField(
        max_length=11,
        required=True,
        validators=[RegexValidator(
            regex=r'^09\d{9}$',
            message='شماره تلفن باید با 09 شروع شود و 11 رقمی باشد.'
        )],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='شماره تلفن'
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number']


class SignUpForm(UserCreationForm, BaseUserForm):
    class Meta(BaseUserForm.Meta):
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'phone_number',  
            'password1', 'password2'
        ]
        labels = {
            'username': 'نام کاربری',
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
       
        self.fields['username'].label = 'نام کاربری'
        self.fields['password1'].label = 'رمز عبور'
        self.fields['password2'].label = 'تکرار رمز عبور'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلاً توسط کاربر دیگری استفاده شده است.')
        
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        User = get_user_model()
        
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('این شماره تلفن قبلاً توسط کاربر دیگری استفاده شده است.')
        
        return phone_number


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='نام کاربری یا ایمیل یا شماره تلفن'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='رمز عبور'
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
            raise forms.ValidationError('این شماره تلفن قبلاً توسط کاربر دیگری استفاده شده است.')
        return phone_number
