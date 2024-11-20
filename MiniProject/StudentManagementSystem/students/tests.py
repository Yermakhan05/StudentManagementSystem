from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from students.models import Student
from django.core.cache import cache
from rest_framework import status

from users.models import CustomUser


class StudentViewSetTests(TestCase):

    def setUp(self):
        self.admin_user = get_user_model().objects.create_user(
            email="admin@test.com",
            password="adminpassword",
            username="admin",
            role="Admin"
        )
        self.teacher_user = get_user_model().objects.create_user(
            email="teacher@test.com",
            password="teacherpassword",
            username="teacher",
            role="Teacher"
        )

        self.student_user = get_user_model().objects.create_user(
            email="student@test.com",
            password="studentpassword",
            username="student",
            role="Student"
        )

        self.student = Student.objects.create(user=self.student_user, dob="2000-01-01")

        self.client = APIClient()

    def test_list_students_with_cache(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/apiStudents/students/')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cache_key = f"students_{self.admin_user.id}"
        cached_data = cache.get(cache_key)
        self.assertIsNotNone(cached_data)

        response2 = self.client.get('/apiStudents/students/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        cached_data2 = cache.get(cache_key)
        self.assertEqual(cached_data, cached_data2)

    def test_create_student_and_cache_clear(self):
        user = CustomUser.objects.create_user(
            role='Admin',
            email="example1@kbtu.kz",
            username='testuser1',
            password='password123'
        )
        self.client.force_authenticate(user=user)
        data = {
            'user': user.id,
            'dob': '2000-01-01',
            'registration_date': '2024-11-20',
            'enrollment_date': '2024-11-21',
        }
        response = self.client.post('/apiStudents/students/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cache_key = f"students_{self.teacher_user.id}"
        cached_data = cache.get(cache_key)
        self.assertIsNone(cached_data)

    def test_update_student_and_cache_clear(self):
        self.client.force_authenticate(user=self.teacher_user)

        data = {
            "user": self.student_user.id,
            "dob": "1999-01-01",
            'registration_date': '2024-11-20',
            'enrollment_date': '2024-11-21',
        }
        response = self.client.patch(f'/apiStudents/students/{self.student.id}/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cache_key = f"students_{self.teacher_user.id}"
        cached_data = cache.get(cache_key)
        self.assertIsNone(cached_data)

    def test_delete_student_and_cache_clear(self):
        self.client.force_authenticate(user=self.teacher_user)

        response = self.client.delete(f'/apiStudents/students/{self.student.id}/')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        cache_key = f"students_{self.teacher_user.id}"
        cached_data = cache.get(cache_key)
        self.assertIsNone(cached_data)
