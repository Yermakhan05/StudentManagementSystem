from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomUserCreateSerializer
import logging
from users.permissions import IsStudent, IsTeacher, IsAdmin

logger = logging.getLogger('custom')


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
