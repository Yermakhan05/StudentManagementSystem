from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Course


@receiver(post_save, sender=Course)
@receiver(post_delete, sender=Course)
def clear_course_cache(sender, instance, **kwargs):
    from django.core.cache import cache
    cache.delete('courses_list')
