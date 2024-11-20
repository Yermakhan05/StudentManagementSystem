from .models import ApiRequestLog, PopularCourse
from .serializers import ApiRequestLogSerializer, PopularCourseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser


class ApiUsageAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        api_logs = ApiRequestLog.objects.all()
        log_serializer = ApiRequestLogSerializer(api_logs, many=True)

        popular_courses = PopularCourse.objects.order_by('-views')[:10]
        course_serializer = PopularCourseSerializer(popular_courses, many=True)

        return Response({
            "api_usage": log_serializer.data,
            "popular_courses": course_serializer.data,
        })
