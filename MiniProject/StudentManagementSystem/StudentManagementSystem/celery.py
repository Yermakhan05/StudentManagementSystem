# project/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagementSystem.settings')

app = Celery('StudentManagementSystem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'send-attendance-reminder': {
#         'task': 'notifications.tasks.send_daily_attendance_reminder',
#         'schedule': crontab(minute=0, hour=9),
#     },
#     'send-grade-update': {
#         'task': 'notifications.tasks.send_grade_update_notification',
#         'schedule': crontab(minute=0, hour=10),
#     },
# }

app.conf.update(
    worker_log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    worker_task_log_format='%(asctime)s - %(task_name)s - %(levelname)s - %(message)s',
)
