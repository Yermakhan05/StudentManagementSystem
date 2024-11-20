# notifications/signals.py
import logging
from celery import shared_task

from grades.models import Grade
from students.models import Student

logger = logging.getLogger('notifications')


@shared_task
def send_daily_attendance_reminder():
    students = Student.objects.all()
    for student in students:
        message = f'Привет, {student.user.username}! Не забудь отметить свое посещение на платформе.'
        logger.info(f"Sending attendance reminder to {student.user.username}: {message}")

    return "Notifications logged successfully"


@shared_task
def send_grade_reminder():
    grades = Grade.objects.all()
    for grade in grades:
        message = f'Привет, {grade.student.user.username}! Тебе поставил {grade.grade} оценок по курсу {grade.course.name}.'
        logger.info(f"Sending grade info reminder to {grade.student.user.username}: {message}")

    return "Notifications logged successfully"

