from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HallViewSet, ClubViewSet, ReviewViewSet, TrainingScheduleViewSet

router = DefaultRouter()
router.register(r'halls', HallViewSet)
router.register(r'clubs', ClubViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'training-schedules', TrainingScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
