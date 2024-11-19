from rest_framework.routers import DefaultRouter
from .views import GradeViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'grades', GradeViewSet, basename='grade')

urlpatterns = [
    path('', include(router.urls)),
]
