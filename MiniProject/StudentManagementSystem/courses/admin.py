from django.contrib import admin
from .models import Course, Enrollment


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'instructor')
    search_fields = ('name', 'instructor__username')


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date')
    list_filter = ('course',)
    search_fields = ('student__name', 'course__name')


admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
