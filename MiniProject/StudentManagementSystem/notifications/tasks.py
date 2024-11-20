from celery import shared_task
from datetime import datetime
from django.core.mail import send_mail
from students.models import Student
from attendance.models import Attendance
from grades.models import Grade
import logging
from celery import shared_task
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

# @shared_task
# def send_daily_attendance_reminder():
#     students = Student.objects.all()
#     for student in students:
#         send_mail(
#             'Ежедневное напоминание о посещаемости',
#             f'Привет, {student.user.username}! Не забудь отметить свое посещение на платформе.',
#             'admin@example.com',
#             [student.user.email],
#             fail_silently=False,
#         )
#
#
# @shared_task
# def send_grade_update_notification(student_id, grade):
#     student = Student.objects.get(id=student_id)
#     send_mail(
#         'Уведомление об изменении оценки',
#         f'Здравствуйте, {student.user.username}. Ваша оценка была обновлена: {grade}.',
#         'admin@example.com',
#         [student.user.email],
#         fail_silently=False,
#     )
