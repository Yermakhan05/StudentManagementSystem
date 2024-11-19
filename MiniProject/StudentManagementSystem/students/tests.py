from django.test import TestCase
from students.models import Student
from users.models import CustomUser


class StudentModelTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(username="teststudent", email="test@example.com")
        Student.objects.create(user=user, dob="2000-01-01")

    def test_student_creation(self):
        student = Student.objects.get(user__username="teststudent")
        self.assertEqual(student.user.email, "test@example.com")
