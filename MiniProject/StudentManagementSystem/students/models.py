from django.db import models
from users.models import CustomUser


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dob = models.DateField(verbose_name="Date of Birth")
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
