from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Course
from .serializers import CourseSerializer
from core.pagination import CustomPageNumberPagination
from users.permissions import IsAdmin, IsTeacherOrAdmin

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['teacher', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'end_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacherOrAdmin()]
        elif self.action == 'list':
            return [IsAdmin()]
        return [IsAdmin()]  # По умолчанию доступ для администратора
