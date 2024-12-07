from django.db import models
from django.core.exceptions import ValidationError

# Опции для выбора вида спорта
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

    def __str__(self):
        return self.name
class Hall(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='hall_images/', verbose_name='Изображение', blank=True, null=True)

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'

    def __str__(self):
        return self.title

# Модель Информации о Зале
class HallInfo(models.Model):
    hall = models.ForeignKey(Hall, related_name='info', on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='hall_images/', verbose_name='Изображение', blank=True, null=True)

    class Meta:
        verbose_name = 'Информация о зале'
        verbose_name_plural = 'Информация о залах'


# Модель Арены Зала
class HallArena(models.Model):
    hall = models.ForeignKey(Hall, related_name='arenas', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название')
    dimensions = models.CharField(max_length=255, verbose_name='Размеры зала')
    capacity = models.CharField(max_length=10, verbose_name='Количество мест')
    type = models.CharField(max_length=100, verbose_name='Тип')
    covering = models.CharField(max_length=100, verbose_name='Покрытие')
    inventory = models.TextField(verbose_name='Инвентарь')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Оплата за час')
    dressing_room = models.BooleanField(verbose_name='Раздевалка', default=False)
    lighting = models.BooleanField(verbose_name='Освещение', default=False)
    shower = models.BooleanField(verbose_name='Душевая', default=False)
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Арена зала'
        verbose_name_plural = 'Арены залов'


class Club(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='clubs')
    title = models.CharField(max_length=255, unique=True, verbose_name='Название клуба')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='club_images/', verbose_name='Изображение', blank=True, null=True)

    class Meta:
        verbose_name = 'Клуб'
        verbose_name_plural = 'Клубы'

class ClubAdditionalInfo(models.Model):
    club = models.ForeignKey(Club, related_name='additional_info', verbose_name='Клуб', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название')
    title1 = models.CharField(max_length=255, verbose_name='Название')
    description1 = models.TextField(verbose_name='Описание')
    title2 = models.CharField(max_length=255, verbose_name='Название')
    description2 = models.TextField(verbose_name='Описание')
    title3 = models.CharField(max_length=255, verbose_name='Название')
    description3 = models.TextField(verbose_name='Описание')
    video_link = models.URLField(max_length=500, verbose_name='Ссылка на видео', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True, null=True)

    class Meta:
        verbose_name = 'Дополнительная информация о клубе'
        verbose_name_plural = 'Дополнительные информации о клубах'

    def __str__(self):
        return self.title1


# Модель Изображения Клуба
class ClubImage(models.Model):
    club = models.ForeignKey(Club, related_name='images', on_delete=models.CASCADE, verbose_name='Клуб')
    additional_info = models.ForeignKey(ClubAdditionalInfo, related_name='images', on_delete=models.CASCADE, verbose_name='Дополнительная информация', null=True, blank=True)
    image = models.ImageField(upload_to='club_images/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение клуба'
        verbose_name_plural = 'Изображения клубов'


# Модель Отзыва
class Review(models.Model):
    user_name = models.CharField(max_length=255, verbose_name='Имя пользователя')
    text = models.TextField(verbose_name='Отзыв')
    rating = models.PositiveIntegerField(verbose_name='Оценка')  # Оценка от 1 до 5
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='reviews', verbose_name="Вид спорта")

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Оценка должна быть от 1 до 5.')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.user_name} на {self.sport.name}'



class HallImage(models.Model):
    hall_info = models.ForeignKey(HallInfo, related_name='images', on_delete=models.CASCADE, verbose_name='Информация о зале')
    image = models.ImageField(upload_to='hall_images/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение зала'
        verbose_name_plural = 'Изображения залов'




# Модель Расписания Тренировок
class TrainingSchedule(models.Model):
    TIME_CHOICES = [
        ('07:00', '07:00'),
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('21:00', '21:00'),
    ]

    DAY_CHOICES = [
        ('Mon', 'Пн'),
        ('Tue', 'Вт'),
        ('Wed', 'Ср'),
        ('Thu', 'Чт'),
        ('Fri', 'Пт'),
        ('Sat', 'Сб'),
    ]

    time = models.CharField(max_length=5, choices=TIME_CHOICES, verbose_name='Время')
    day = models.CharField(max_length=3, choices=DAY_CHOICES, verbose_name='День')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name="Вид спорта")
    age_group = models.CharField(max_length=255, verbose_name='Возрастная группа')
    coach = models.CharField(max_length=255, verbose_name='Тренер')

    class Meta:
        verbose_name = 'Расписание тренировки'
        verbose_name_plural = 'Расписания тренировок'

    def __str__(self):
        return f'{self.day} {self.time} - {self.sport.name} ({self.age_group}) - {self.coach}'
