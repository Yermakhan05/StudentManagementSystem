from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'date_sent', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('message', )


admin.site.register(Notification, NotificationAdmin)
