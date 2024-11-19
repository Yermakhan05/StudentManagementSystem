from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Student
from .serializers import StudentSerializer
from core.pagination import CustomPageNumberPagination
from users.permissions import IsAdmin, IsTeacher, IsStudent

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['enrolled_courses', 'grade']
    search_fields = ['user__username', 'user__email']
    ordering_fields = ['date_joined', 'grade']

    def get_permissions(self):
        if self.action == 'list': 
            return [IsAdmin()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacher()]
        if self.action == 'retrieve': 
            return [IsStudent()]
        return [IsAdmin()]  
