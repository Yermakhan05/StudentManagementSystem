from django.contrib import admin
from .models import ApiRequestLog, PopularCourse


class ApiRequestLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'endpoint', 'timestamp',)
    list_filter = ('user', 'endpoint')


admin.site.register(ApiRequestLog, ApiRequestLogAdmin)


class PopularCourseAdmin(admin.ModelAdmin):
    list_display = ('course', 'views')
    list_filter = ('course',)


admin.site.register(PopularCourse, PopularCourseAdmin)
