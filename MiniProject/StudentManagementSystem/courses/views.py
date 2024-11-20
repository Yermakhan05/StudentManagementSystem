from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.pagination import CustomPageNumberPagination
from students.models import Student
from .models import Course
from .serializers import CourseSerializer
from users.permissions import IsAdmin, IsTeacherOrAdmin, IsStudent
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all().order_by('id')
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'instructor']
    ordering_fields = ['start_date', 'end_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacherOrAdmin()]
        elif self.action == 'list':
            if self.request.user.role == "Admin":
                return [IsAdmin()]
            elif self.request.user.role == "Teacher":
                return [IsTeacherOrAdmin()]
            elif self.request.user.role == "Student":
                return [IsStudent()]
        elif self.action == 'retrieve':
            return [IsStudent(), IsTeacherOrAdmin()]
        return []

    @swagger_auto_schema(
        operation_description="Получить список всех курсов.",
        responses={
            200: openapi.Response(
                description="Список курсов.",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "name": "Mathematics",
                            "description": "A basic math course.",
                            "instructor": 1,
                            "start_date": "2024-01-01",
                            "end_date": "2024-06-01"
                        },
                        {
                            "id": 2,
                            "name": "Physics",
                            "description": "An introductory physics course.",
                            "instructor": 2,
                            "start_date": "2024-02-01",
                            "end_date": "2024-07-01"
                        }
                    ]
                },
            )
        },
    )

    def list(self, request, *args, **kwargs):
        user = request.user
        cache_key = f"courses_{user.id}"
        cached_courses = cache.get(cache_key)

        if cached_courses:
            return Response(cached_courses)

        if user.role == "Teacher":
            courses = self.queryset.filter(instructor=user)
        elif user.role == "Student":
            student = Student.objects.filter(user=user).first()
            if not student:
                return Response({"detail": "Student profile not found."}, status=404)
            courses = self.queryset.filter(enrollment__student=student)
        else:
            courses = self.queryset

        page = self.paginate_queryset(courses)
        if page is not None:
            serialized_page = self.get_serializer(page, many=True)
            cache.set(cache_key, serialized_page.data, timeout=3600)
            return self.get_paginated_response(serialized_page.data)

        serialized_data = self.get_serializer(courses, many=True).data
        cache.set(cache_key, serialized_data, timeout=3600)
        return Response(serialized_data)

    @swagger_auto_schema(
        operation_description="Создать новый курс.",
        request_body=CourseSerializer,
        responses={
            201: openapi.Response(
                description="Курс успешно создан.",
                examples={
                    "application/json": {
                        "id": 3,
                        "name": "Biology",
                        "description": "Introduction to Biology.",
                        "instructor": 3,
                        "start_date": "2024-03-01",
                        "end_date": "2024-08-01"
                    }
                },
            )
        },
    )

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache.delete_pattern("courses_*")
        return response

    @swagger_auto_schema(
        operation_description="Удалить курс.",
        responses={
            204: openapi.Response(description="Курс успешно удален."),
            403: "Доступ запрещен."
        },
    )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache.delete_pattern("courses_*")
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete_pattern("courses_*")
        return response
