import django_filters
from .models import *

class HallFilter(django_filters.FilterSet):
    sports = django_filters.ChoiceFilter(field_name='sports', choices=Hall.SPORT_CHOICES, label="Виды спорта")
    title = django_filters.CharFilter(lookup_expr='icontains', label="имя")
    class Meta:
        model = Hall
        fields = ['sports','title']

class AdvertisementFilter(django_filters.FilterSet):
    phone = django_filters.CharFilter(lookup_expr='icontains', label="Телефон")
    title = django_filters.CharFilter(lookup_expr='icontains', label="имя")
    # Добавьте другие фильтры по необходимости

    class Meta:
        model = Advertisement
        fields = ['phone', 'title']  #

class CircleFilter(django_filters.FilterSet):
    sports = django_filters.ChoiceFilter(field_name='sports', choices=Hall.SPORT_CHOICES, label="Виды спорта")
    title = django_filters.CharFilter(lookup_expr='icontains', label="Имя")
    class Meta:
        model = Circle
        fields = ['sports', 'title']


class TrainerFilter(django_filters.FilterSet):
    sports = django_filters.ChoiceFilter(field_name='sports', choices=Hall.SPORT_CHOICES, label="Виды спорта")
    first_name = django_filters.CharFilter(lookup_expr='icontains', label="Имя")
    email = django_filters.CharFilter(lookup_expr='icontains', label="Электронная почта")
    class Meta:
        model = Trainer  # Указываем модель тренера
        fields = ['sports', 'first_name', 'email']

class ClientFilter(django_filters.FilterSet):
    PAYMENT_METHOD_CHOICES = [
        ('Наличные', 'Наличные'),
        ('Карта', 'Карта'),
        ( 'Перевод', 'Перевод'),
    ]
    name = django_filters.CharFilter(lookup_expr='icontains', label="Имя")
    trainer = django_filters.ModelChoiceFilter(queryset=Trainer.objects.all(), label="Тренер")
    sports = django_filters.ChoiceFilter(field_name='sports', choices=Hall.SPORT_CHOICES, label="Виды спорта")
    payment_method = django_filters.ChoiceFilter(choices=PAYMENT_METHOD_CHOICES, label="Метод оплаты")
    class Meta:
        model = Client  # Указываем модель клиента
        fields = ['name', 'trainer', 'sports', 'payment_method']  # Перечисляем поля для фильтрации

class ReviewhallFilter(django_filters.FilterSet):
    hall = django_filters.ModelChoiceFilter(queryset=Hall.objects.all(), label='Зал')
    name = django_filters.CharFilter(lookup_expr='icontains', label="Имя")

    class Meta:
        model = Reviewhall
        fields = ['hall', 'name']
class PaymentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label="Имя")
    sport = django_filters.ChoiceFilter(field_name='sport', choices=Hall.SPORT_CHOICES, label="Виды спорта")

    class Meta:
        model = Payment  # Укажите модель, по которой нужно фильтровать
        fields = ['name', 'sport']
class ReviewcircleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label="Имя")
    circle = django_filters.ModelChoiceFilter(queryset=Circle.objects.all(), label="Кружок")  # Фильтр по кружку

    class Meta:
        model = Reviewcircle
        fields = ['name', 'circle']