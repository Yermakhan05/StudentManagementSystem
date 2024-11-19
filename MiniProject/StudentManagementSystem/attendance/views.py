from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from students.models import Student
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsTeacher
from celery import shared_task
from django.core.mail import send_mail


class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update']:
            return [IsAuthenticated(), IsTeacher()]
        return [IsAuthenticated()]


@shared_task
def send_attendance_reminder():
    students = Student.objects.all()
    for student in students:
        send_mail(
            "Daily Attendance Reminder",
            "Please mark your attendance for today.",
            "admin@example.com",
            [student.user.email],
        )
    return "Reminders Sent"
