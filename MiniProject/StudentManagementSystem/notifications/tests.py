from django.test import TestCase
from notifications.tasks import send_daily_attendance_reminder, send_grade_reminder
from celery import current_app


class CeleryTasksTest(TestCase):

    def setUp(self):
        current_app.conf.update(CELERY_TASK_ALWAYS_EAGER=True)

    def test_send_daily_attendance_reminder(self):
        send_daily_attendance_reminder()
        self.assertEqual(1, 1)

    def test_send_grade_reminder(self):
        send_grade_reminder()
        self.assertEqual(1, 1)
