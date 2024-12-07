from rest_framework import serializers
from .models import *

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'  # Specify fields explicitly


class BankCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCard
        fields = ['id', 'cardholder_name', 'card_number', 'expiry_date', 'cvc_code']
        extra_kwargs = {
            'card_number': {'write_only': True},
            'cvc_code': {'write_only': True}
        }


class Payment1Serializer(serializers.ModelSerializer):
    payment_method = BankCardSerializer(read_only=True)

    class Meta:
        model = Payment1
        fields = ['id', 'sport', 'monthly_price', 'paid', 'payment_method']
