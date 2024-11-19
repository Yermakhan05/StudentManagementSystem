from django.contrib import admin
from .models import Student


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'registration_date')
    list_filter = ('registration_date',)
    search_fields = ('email',)


admin.site.register(Student, StudentAdmin)
