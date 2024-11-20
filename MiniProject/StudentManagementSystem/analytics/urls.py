from django.urls import path
from .views import ApiUsageAnalyticsView

urlpatterns = [
    path('api/analytics/', ApiUsageAnalyticsView.as_view(), name='api-analytics'),
]
