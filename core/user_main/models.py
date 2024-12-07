from django.db import models

class SportClass(models.Model):
    SPORT_CHOICES = [
        ('Баскетбол', 'Баскетбол'),
        ('Футбол', 'Футбол'),
        ('Теннис', 'Теннис'),
        ('Плавание', 'Плавание'),
        ('Волейбол', 'Волейбол'),
        ('Тхэквондо', 'Тхэквондо'),
        ('Бокс', 'Бокс'),
        ('Велоспорт', 'Велоспорт'),
        ('Йога', 'Йога'),
    ]

    HALL_CHOICES = [
        ('Основной зал', 'Основной зал'),
        ('Вторичный зал', 'Вторичный зал'),
        ('Уличная площадка', 'Уличная площадка'),
    ]

    CIRCLE = [
        ('Начинающий', 'Начинающий'),
        ('Средний', 'Средний'),
        ('Продвинутый', 'Продвинутый'),
    ]

    sport_type = models.CharField(max_length=50, choices=SPORT_CHOICES)
    class_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    schedule = models.CharField(max_length=255, blank=True, null=True)
    img = models.ImageField(blank=True, null=True, upload_to='class_images/')

    hall_type = models.CharField(max_length=50, choices=HALL_CHOICES, blank=True, null=True)
    circle = models.CharField(max_length=50, choices=CIRCLE, blank=True, null=True)

    def __str__(self):
        return self.class_name

    def save(self, *args, **kwargs):
        # Если у модели уже есть первичный ключ (то есть, она уже существует)
        if self.pk:
            old_instance = SportClass.objects.get(pk=self.pk)
            # Если новое изображение не предоставлено, сохранить старое
            if not self.img:
                self.img = old_instance.img

        # Вызвать стандартный метод сохранения
        super().save(*args, **kwargs)
class GymInfo(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    instagram = models.URLField(blank=True, null=True)
    installment_options = models.CharField(max_length=100)  # "6/9/12 месяцев"

    # и любые другие поля, которые вам нужны

    def __str__(self):
        return self.name