import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

logger = logging.getLogger('django')


@receiver(post_save, sender=CustomUser)
def log_user_registration(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Новый пользователь зарегистрирован: {instance.email}, роль: {instance.role}")


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f"Пользователь вошел в систему: {user.email}")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    logger.info(f"Пользователь вышел из системы: {user.email}")
