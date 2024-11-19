from django.contrib import admin
from .models import Grade


class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade', 'date', 'teacher')
    list_filter = ('course', 'teacher')
    search_fields = ('student__name', 'course__name', 'teacher__username')


admin.site.register(Grade, GradeAdmin)
