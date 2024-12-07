from rest_framework import generics
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser

class SportClassListCreateView(generics.ListCreateAPIView):
    queryset = SportClass.objects.all()
    serializer_class = SportClassSerializer
    filter_backends = [DjangoFilterBackend]
    parser_classes = [MultiPartParser]
    filterset_fields = ['sport_type', 'schedule']


class SportClassRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SportClass.objects.all()
    serializer_class = SportClassSerializer
    parser_classes = [MultiPartParser]

class GymInfoView(generics.RetrieveAPIView):
    queryset = GymInfo.objects.all()
    serializer_class = GymInfoSerializer
    parser_classes = [MultiPartParser]

    def get_object(self):
        return GymInfo.objects.first()