from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    #
    # objects = CustomUserManager()

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
