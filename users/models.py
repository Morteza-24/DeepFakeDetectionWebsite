from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        verbose_name='شماره تلفن',
        validators=[RegexValidator(
            regex=r'^09\d{9}$',
            message='شماره تلفن باید با 09 شروع شود و 11 رقمی باشد.'
        )]
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.email
