import datetime
from analytics.models import ApiRequestLog, PopularCourse
from courses.models import Course


class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api'):
            user = request.user if request.user.is_authenticated else None
            ApiRequestLog.objects.create(user=user, endpoint=request.path)

            if request.path.startswith('/apiCourses/') and request.method == "GET":
                course_id = request.GET.get('course_id')
                if course_id:
                    course, created = PopularCourse.objects.get_or_create(course_id=course_id)
                    course.views += 1
                    course.save()

        response = self.get_response(request)
        return response
