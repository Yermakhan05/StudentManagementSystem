from django.db.models.signals import post_delete
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Enrollment, Course

logger = logging.getLogger('courses')


@receiver(post_save, sender=Enrollment)
def log_course_enrollment(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Студент {instance.student.user.username} записан на курс {instance.course.name}")


@receiver(post_save, sender=Course)
@receiver(post_delete, sender=Course)
def clear_course_cache(sender, instance, **kwargs):
    from django.core.cache import cache
    cache.delete('courses_list')
