from rest_framework import serializers
from .models import *


class SportClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportClass
        fields = '__all__'


class GymInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymInfo
        fields = '__all__'