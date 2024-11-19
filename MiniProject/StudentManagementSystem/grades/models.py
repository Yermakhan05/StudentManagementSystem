from django.db import models
from students.models import Student
from courses.models import Course
from users.models import CustomUser
from celery import shared_task
from django.core.mail import send_mail


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Teacher'})

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} - {self.grade}"


@shared_task
def notify_grade_update(student_email, course_name, grade):
    send_mail(
        "Grade Updated",
        f"Your grade for {course_name} has been updated to {grade}.",
        "admin@example.com",
        [student_email],
    )
