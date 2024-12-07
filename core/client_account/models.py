from django.db import models
from django.conf import settings  # Импортируем settings для использования кастомной модели пользователя
from django.contrib.auth.models import User

SPORT_CHOICES = [
    ('basketball', 'Баскетбол'),
    ('football', 'Футбол'),

    ('tennis', 'Теннис'),
    ('swimming', 'Плавание'),
    ('volleyball', 'Волейбол'),
    ('taekwondo', 'Тхэквондо'),
    ('boxing', 'Бокс'),
    ('cycling', 'Велоспорт'),
    ('yoga', 'Йога'),
]

# Модель Спорта
class Sport(models.Model):
    name = models.CharField(max_length=50, choices=SPORT_CHOICES, verbose_name="Вид спорта")

    class Meta:
        verbose_name = 'Вид спорта'
        verbose_name_plural = 'Виды спорта'


class Schedule(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.sport.name} - {self.date}"


class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)  # Ссылка на кастомную модель пользователя
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.schedule}"

class Payment1(models.Model):
    SPORTS_CHOICES = [
        ('баскетбол', 'Баскетбол'),
        ('футбол', 'Футбол'),
        ('волейбол', 'Волейбол'),
        ('теннис', 'Тенис'),
        ('бокс', 'Бокс'),
        ('велоспорт', 'Велоспорт'),
        ('таэквондо', 'Таэквондо'),
        ('плавание', 'Плавание'),
        ('йога', 'Йога'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sport = models.CharField(verbose_name='Виды спорта', max_length=100, choices=SPORTS_CHOICES)
    paid = models.BooleanField(default=False, verbose_name="Оплачено")
    enrollment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата записи")
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за месяц")
    payment_method = models.ForeignKey('BankCard', on_delete=models.SET_NULL, null=True, blank=True,verbose_name="Способ оплаты")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class BankCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiration_date = models.DateField()
    cardholder_name = models.CharField(max_length=100, verbose_name="Имя владельца карты")
    card_number = models.CharField(max_length=16, verbose_name="Номер карты")
    expiry_date = models.CharField(max_length=5, verbose_name="Дата истечения срока действия (MM/YY)")
    cvc_code = models.CharField(max_length=3, verbose_name="CVC/CVV код")
    added_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Банковская карта"
        verbose_name_plural = "Банковские карты"

    def __str__(self):
        return f"{self.cardholder_name} - {self.card_number[-4:]}"

