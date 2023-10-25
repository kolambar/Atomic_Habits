from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


NULLABLE = {'blank': True, 'null': True}


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, telegram=None, **extra_fields):  # метод переопределяется, чтобы не нужно было username

        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, telegram=telegram, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    telegram = models.URLField(verbose_name='ссылка на телеграмм', **NULLABLE, max_length=200)
    telegram_id = models.CharField(verbose_name='id телеграмма', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # нужна кастомная настройка, так как для регистрации не подойдет обычная.
    objects = CustomUserManager()
