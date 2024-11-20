from django.core.cache import cache
from students.models import Student
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from grades.models import Grade
from attendance.models import Attendance

logger = logging.getLogger('students')


@receiver(post_save, sender=Attendance)
def log_attendance(sender, instance, created, **kwargs):
    if created:
        logger.info(
            f"Attendance {instance.status} выставлена студенту {instance.student.user.username} за курс {instance.course.name}")


@receiver(post_save, sender=Grade)
def log_grade_updated(sender, instance, **kwargs):
    logger.info(f"Оценка обновлена для студента {instance.student.user.username}: новый балл {instance.grade}")


@receiver(post_save, sender=Student)
def clear_student_cache(sender, instance, **kwargs):
    cache_key = f"courses_{instance.user.id}"
    cache.delete(cache_key)
