from django.contrib import admin
from .models import *

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('sport', 'date', 'price')

    def sport(self, obj):
        return obj.sport.name

    sport.short_description = 'Спорт'

@admin.register(Payment1)
class Payment1Admin(admin.ModelAdmin):
    list_display = ('user', 'sport', 'monthly_price', 'paid', 'enrollment_date', 'payment_method')
    list_filter = ('paid', 'sport', 'enrollment_date')
    search_fields = ('user__username', 'sport')
    ordering = ('-enrollment_date',)

@admin.register(BankCard)
class BankCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'cardholder_name', 'card_number_display', 'expiry_date', 'added_date')
    search_fields = ('user__username', 'cardholder_name')
    readonly_fields = ('card_number_display',)

    def card_number_display(self, obj):
        # Показывает только последние 4 цифры для безопасности
        return f"**** **** **** {obj.card_number[-4:]}"
    card_number_display.short_description = 'Номер карты'


# Регистрация модели Payment1 с администратором