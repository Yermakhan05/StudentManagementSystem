from django.db import models
from students.models import Student
from courses.models import Course


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} - {self.status} on {self.date}"
