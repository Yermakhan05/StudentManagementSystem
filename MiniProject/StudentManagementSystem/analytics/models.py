from django.db import models
from users.models import CustomUser
from courses.models import Course


class ApiRequestLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    endpoint = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class PopularCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
