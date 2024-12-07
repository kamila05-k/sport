from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Hall, Club, Review, TrainingSchedule
from .serializers import HallSerializer, ClubSerializer, ReviewSerializer, TrainingScheduleSerializer
from .filters import HallFilter, ClubFilter, ReviewFilter, TrainingScheduleFilter

class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HallFilter  # Use HallFilter

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [AllowAny()]
        return super().get_permissions()

class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClubFilter  # Use ClubFilter

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [AllowAny()]
        return super().get_permissions()

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter  # Use ReviewFilter

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [AllowAny()]
        return super().get_permissions()

class TrainingScheduleViewSet(viewsets.ModelViewSet):
    queryset = TrainingSchedule.objects.all()
    serializer_class = TrainingScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TrainingScheduleFilter  # Use TrainingScheduleFilter

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [AllowAny()]
        return super().get_permissions()
