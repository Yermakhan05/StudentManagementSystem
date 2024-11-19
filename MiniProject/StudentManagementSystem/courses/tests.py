from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

# Используем CustomUser вместо стандартной User
User = get_user_model()

class CourseAPITestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей с разными ролями
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='admin123',
            role='Admin'  # Поле role определено в CustomUser
        )
        self.teacher_user = User.objects.create_user(
            username='teacher',
            email='teacher@test.com',
            password='teacher123',
            role='Teacher'
        )
        self.student_user = User.objects.create_user(
            username='student',
            email='student@test.com',
            password='student123',
            role='Student'
        )

    def test_role_based_access(self):
        # Аутентификация как студент
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get('/api/courses/')  # Эндпоинт для курсов

        # Студенту доступ запрещен
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
