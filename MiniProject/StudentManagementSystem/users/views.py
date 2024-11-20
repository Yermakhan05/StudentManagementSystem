from rest_framework.views import APIView
from .serializers import CustomUserCreateSerializer
from users.permissions import IsStudent, IsTeacher, IsAdmin
import logging
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

logger = logging.getLogger('django')


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            logger.info(f"Пользователь с email вошел в систему.")
        else:
            logger.warning("Ошибка аутентификации при получении токенов.")

        return response


class StudentOnlyView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        return Response({"message": "Welcome, Student!"})


class TeacherOnlyView(APIView):
    permission_classes = [IsTeacher]

    def get(self, request):
        return Response({"message": "Welcome, Teacher!"})


class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"message": "Welcome, Admin!"})


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User registered: {user.username}")
            return Response({"message": "User registered successfully!"})
        return Response(serializer.errors, status=400)
