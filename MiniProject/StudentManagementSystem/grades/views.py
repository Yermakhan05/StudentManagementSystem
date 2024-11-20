from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Grade
from .serializers import GradeSerializer
from users.permissions import IsTeacher
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), IsTeacher()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="Получить список оценок.",
        responses={
            200: openapi.Response(
                description="Успешный запрос.",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "student": 1,
                            "course": 1,
                            "grade": "A",
                            "date": "2024-11-20",
                            "teacher": 2,
                        },
                        {
                            "id": 2,
                            "student": 2,
                            "course": 1,
                            "grade": "B",
                            "date": "2024-11-19",
                            "teacher": 3,
                        }
                    ]
                },
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новую оценку.",
        request_body=GradeSerializer,
        responses={
            201: openapi.Response(
                description="Оценка успешно создана.",
                examples={
                    "application/json": {
                        "id": 3,
                        "student": 1,
                        "course": 2,
                        "grade": "A",
                        "date": "2024-11-20",
                        "teacher": 2,
                    }
                },
            ),
            403: "Доступ запрещен.",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)