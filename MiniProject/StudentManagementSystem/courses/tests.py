from datetime import date

from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache

from students.models import Student
from users.models import CustomUser
from courses.models import Course, Enrollment


class CourseViewSetTests(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            username="admin_user",
            role="Admin",
            email="admin1212@kbtu.kz",
            password="password123"
        )
        self.teacher = CustomUser.objects.create_user(
            username="teacher_user",
            role="Teacher",
            email="teacher1212@kbtu.kz",
            password="password123"
        )
        self.student = CustomUser.objects.create_user(
            email="student212@kbtu.kz",
            password="password123",
            role="Student",
            username="kasym",
        )
        self.student_1 = Student.objects.create(user=self.student, dob="2005-01-20")

        self.course1 = Course.objects.create(
            name="Course 1",
            description="Advanced Math Course",
            instructor=self.teacher,
            start_date=date(2024, 11, 1),
            end_date=date(2024, 12, 31)
        )
        self.course2 = Course.objects.create(
            name="Course 2",
            description="Advanced android Course",
            instructor=self.teacher,
            start_date=date(2024, 11, 1),
            end_date=date(2024, 12, 31)
        )

        self.client.force_authenticate(user=self.admin)

    def test_list_courses_with_cache(self):
        cache_key = f"courses_{self.admin.id}"
        cache.delete(cache_key)

        response = self.client.get("/apiCourses/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cached_data = cache.get(cache_key)
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)

        response_cached = self.client.get("/apiCourses/courses/")
        self.assertEqual(response_cached.status_code, status.HTTP_200_OK)
        self.assertEqual(response_cached.data, cached_data)

    def test_permissions_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/apiCourses/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permissions_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get("/apiCourses/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_permissions_student(self):
        Enrollment.objects.create(student=self.student_1, course=self.course1)
        self.client.force_authenticate(user=self.student)
        response = self.client.get("/apiCourses/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_create_course(self):
        self.client.force_authenticate(user=self.teacher)
        data = {
            "name": "Course 3",
            "description": "Advanced iOS Course",
            "instructor": self.teacher.id,
            "start_date": "2024-11-01",
            "end_date": "2024-12-31"
        }
        response = self.client.post("/apiCourses/courses/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Course 3")

    def test_update_course(self):
        self.client.force_authenticate(user=self.teacher)
        data = {"name": "Updated Course"}
        response = self.client.patch(f"/apiCourses/courses/{self.course1.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course1.refresh_from_db()
        self.assertEqual(self.course1.name, "Updated Course")

    def test_destroy_course(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(f"/apiCourses/courses/{self.course1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=self.course1.id).exists())

    def test_cache_invalidation_on_update(self):
        cache_key = f"courses_{self.admin.id}"
        cache.set(cache_key, [{"name": "Old Course"}], timeout=3600)

        self.client.force_authenticate(user=self.teacher)
        data = {"name": "Updated Course"}
        response = self.client.patch(f"/apiCourses/courses/{self.course1.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNone(cache.get(cache_key))

    def test_cache_invalidation_on_delete(self):
        cache_key = f"courses_{self.admin.id}"
        cache.set(cache_key, [{"name": "Old Course"}], timeout=3600)

        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(f"/apiCourses/courses/{self.course1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertIsNone(cache.get(cache_key))
