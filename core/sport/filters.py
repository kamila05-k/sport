from django_filters import rest_framework as filters
from .models import *

class HallFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='sport_id')

    class Meta:
        model = Hall
        fields = ['id']

class ClubFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='sport_id')

    class Meta:
        model = Club
        fields = ['id']

# Фильтр для отзывов
class ReviewFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='sport_id')

    class Meta:
        model = Review
        fields = ['id']

# Фильтр для расписания тренировок
class TrainingScheduleFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='sport_id')

    class Meta:
        model = TrainingSchedule
        fields = ['id']
