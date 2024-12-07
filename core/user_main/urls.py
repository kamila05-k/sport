from django.urls import path
from .views import SportClassListCreateView, SportClassRetrieveUpdateDestroyView, GymInfoView

urlpatterns = [
    path('sport-classes/', SportClassListCreateView.as_view(), name='sportclass-list-create'),
    path('sport-classes/<int:pk>/', SportClassRetrieveUpdateDestroyView.as_view(), name='sportclass-detail'),
    path('gym-info/', GymInfoView.as_view(), name='gym-info'),

]