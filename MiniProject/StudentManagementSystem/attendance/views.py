from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from students.models import Student
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsTeacher
from celery import shared_task
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update']:
            return [IsAuthenticated(), IsTeacher()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="Получить список всех записей посещаемости.",
        responses={
            200: openapi.Response(
                description="Список записей посещаемости.",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "student": 1,
                            "course": 2,
                            "date": "2024-11-01",
                            "status": "Present"
                        },
                        {
                            "id": 2,
                            "student": 3,
                            "course": 4,
                            "date": "2024-11-02",
                            "status": "Absent"
                        }
                    ]
                },
            )
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать запись о посещаемости.",
        request_body=AttendanceSerializer,
        responses={
            201: openapi.Response(
                description="Запись успешно создана.",
                examples={
                    "application/json": {
                        "id": 3,
                        "student": 5,
                        "course": 6,
                        "date": "2024-11-03",
                        "status": "Present"
                    }
                },
            )
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить запись о посещаемости.",
        request_body=AttendanceSerializer,
        responses={
            200: openapi.Response(
                description="Запись успешно обновлена.",
                examples={
                    "application/json": {
                        "id": 3,
                        "student": 5,
                        "course": 6,
                        "date": "2024-11-03",
                        "status": "Absent"
                    }
                },
            )
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить запись о посещаемости.",
        responses={
            204: openapi.Response(description="Запись успешно удалена."),
            403: "Доступ запрещен."
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


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
