from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
import logging
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class BankCardListCreateView(generics.ListCreateAPIView):
    queryset = BankCard.objects.all()
    serializer_class = BankCardSerializer

class Payment1ListView(generics.ListAPIView):
    serializer_class = Payment1Serializer
    queryset = Payment1.objects.all()
