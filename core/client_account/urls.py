from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register(r'schedules', ScheduleViewSet)
router.register(r'attendances', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bank-cards/', BankCardListCreateView.as_view(), name='bank-card-list-create'),
    path('payments/', Payment1ListView.as_view(), name='payment-list'),
]
