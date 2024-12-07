from rest_framework import serializers
from .models import Sport, Hall, HallInfo, HallArena, Club, ClubAdditionalInfo, ClubImage, Review, HallImage, TrainingSchedule
from django_filters import rest_framework as filters

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ['id', 'name']

class HallImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallImage
        fields = ['id', 'image']

class HallInfoSerializer(serializers.ModelSerializer):
    sport = filters.CharFilter(field_name='sport', lookup_expr='exact')

    class Meta:
        model = HallInfo
        fields = '__all__'

class HallArenaSerializer(serializers.ModelSerializer):
    sport = filters.CharFilter(field_name='sport', lookup_expr='exact')
    hall_info = HallInfoSerializer(many=True, read_only=True, source='hall.hall_info')  # Получение информации о зале

    class Meta:
        model = HallArena
        fields = '__all__'

class HallSerializer(serializers.ModelSerializer):
    images = HallImageSerializer(many=True, read_only=True)
    arenas = HallArenaSerializer(many=True, read_only=True)  # Связанные арены зала
    info = HallInfoSerializer(many=True, read_only=True)
    sport = filters.CharFilter(field_name='sport', lookup_expr='exact')

    class Meta:
        model = Hall
        fields = '__all__'



class ClubImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubImage
        fields = ['id', 'image']

class ClubAdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubAdditionalInfo
        fields = '__all__'  # Возвращаем все поля

class ClubSerializer(serializers.ModelSerializer):
    images = ClubImageSerializer(many=True, read_only=True)
    additional_info = ClubAdditionalInfoSerializer(many=True, read_only=True)
    sport = filters.CharFilter(field_name='sport', lookup_expr='exact')  # Применяем фильтр на sport

    class Meta:
        model = Club
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    sport = filters.CharFilter(field_name='sport', lookup_expr='exact')
    class Meta:
        model = Review
        fields = '__all__'


class TrainingScheduleSerializer(serializers.ModelSerializer):
    sport = filters.CharFilter(field_name='sport', lookup_expr='exact')
    class Meta:
        model = TrainingSchedule
        fields = '__all__'
