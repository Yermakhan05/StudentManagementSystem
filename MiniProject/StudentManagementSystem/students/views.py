from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from core.pagination import CustomPageNumberPagination
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsAdmin, IsTeacherOrAdmin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all().order_by('id')
    serializer_class = StudentSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['grade', 'enrollment_date']
    search_fields = ['user__username', 'user__email']
    ordering_fields = ['enrollment_date', 'grade']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacherOrAdmin()]
        elif self.action == 'list':
            return [IsTeacherOrAdmin(), IsAdmin()]
        elif self.action == 'retrieve':
            return [IsTeacherOrAdmin(), IsAdmin()]
        return [IsAdmin()]

    @swagger_auto_schema(
        operation_description="Получение списка студентов для учителей или администраторов",
        responses={
            200: openapi.Response(
                description="Список студентов",
                examples={
                    "application/json": {
                        "students": [
                            {"id": 1, "name": "John Doe", "grade": "A"},
                            {"id": 2, "name": "Jane Smith", "grade": "B"}
                        ]
                    }
                },
            ),
            403: "Access denied",
        },
    )

    def list(self, request, *args, **kwargs):
        user = request.user
        cache_key = f"students_{user.id}"
        cached_students = cache.get(cache_key)

        if cached_students:
            return Response(cached_students)

        if user.role == "Teacher":
            students = self.queryset.filter(grade__teacher=user)
        elif user.role == "Admin":
            students = self.queryset
        else:
            return Response({"detail": "Access denied."}, status=403)

        page = self.paginate_queryset(students)
        if page is not None:
            serialized_page = self.get_serializer(page, many=True)
            cache.set(cache_key, serialized_page.data, timeout=3600)
            return self.get_paginated_response(serialized_page.data)

        serialized_data = self.get_serializer(students, many=True).data
        cache.set(cache_key, serialized_data, timeout=3600)
        return Response(serialized_data)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache.delete_pattern("students_*")
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache.delete_pattern("students_*")
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete_pattern("students_*")
        return response
