from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    first_name = models.CharField(
        max_length=50,
        verbose_name=_('نام')
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name=_('نام خانوادگی')
    )
    email = models.EmailField(
        unique=True,
        verbose_name=_('ایمیل')
    )
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        verbose_name=_('شماره تلفن'),
        validators=[RegexValidator(
            regex=r'^09\d{9}$',
            message=_('شماره تلفن باید با 09 شروع شود و 11 رقمی باشد.')  
        )]
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'username']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)