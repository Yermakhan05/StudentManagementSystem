from rest_framework import serializers
from .models import ApiRequestLog, PopularCourse


class ApiRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiRequestLog
        fields = ['user', 'endpoint', 'timestamp']


class PopularCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularCourse
        fields = ['course', 'views']
