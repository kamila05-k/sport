from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, FileExtensionValidator
from django.template.base import filter_raw_string

class Hall(models.Model):
    SPORT_CHOICES = [
        ('Баскетбол', 'Баскетбол'),
        ('Футбол', 'Футбол'),
        ('Волейбол', 'Волейбол'),
        ('Тенис', 'Тенис'),
        ('Бокс', 'Бокс'),
        ('Велоспорт', 'Велоспорт'),
        ('Таэквондо', 'Таэквондо'),
        ('Плавание', 'Плавание'),
        ('Йога', 'Йога'),
    ]
    sports = models.CharField(verbose_name='Виды спорта', max_length=20, choices=SPORT_CHOICES)
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    description = models.TextField(verbose_name='Описание')
    phone = models.CharField(verbose_name='Телефон', max_length=20)
    address = models.CharField(verbose_name='Адрес', max_length=255)
    size = models.CharField(verbose_name='Размеры', max_length=50)
    inventory = models.TextField(verbose_name='Инвентарь')
    price_per_hour = models.DecimalField(verbose_name='Оплата за час', max_digits=10, decimal_places=2)
    quantity = models.IntegerField(verbose_name='Количество')
    coverage = models.CharField(verbose_name='Покрытие', max_length=100)
    hall_type = models.CharField(verbose_name='Тип', max_length=100)
    shower = models.BooleanField(default=False, verbose_name='Душевая')
    lighting = models.BooleanField(default=False, verbose_name='Освещение')
    dressing_room = models.BooleanField(default=False, verbose_name='Раздевалка')
    image = models.ImageField(upload_to='hall_images/',blank=True, null=True)
    image1 = models.ImageField(upload_to='hall_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='hall_images/',blank=True, null=True)
    image3 = models.ImageField(upload_to='hall_images/',blank=True, null=True)
    def __str__(self):
        return f"{self.id} - {self.title}"
    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'

    def save(self, *args, **kwargs):
        if self.pk:  # Эгер жазуу мурунтан болсо
            old_hall = Hall.objects.get(pk=self.pk)
            # Эгер жаңы сүрөттөр жүктөлбөсө, эски сүрөттөрдү сактап калуу
            self.image = self.image or old_hall.image
            self.image1 = self.image1 or old_hall.image1
            self.image2 = self.image2 or old_hall.image2
            self.image3 = self.image3 or old_hall.image3
        super().save(*args, **kwargs)
class WorkSchedule(models.Model):
    hall = models.ForeignKey(
        Hall,
        related_name='schedules',
        on_delete=models.CASCADE,
        verbose_name="Зал"
    )
    day_of_week = models.CharField(
        max_length=12,
        choices=[
            ('Понедельник', 'Понедельник'),
            ('Вторник', 'Вторник'),
            ('Среда', 'Среда'),
            ('Четверг', 'Четверг'),
            ('Пятница', 'Пятница'),
            ('Суббота', 'Суббота'),
            ('Воскресенье', 'Воскресенье'),
        ],
        verbose_name="День недели",
        blank=True,  # Поле не обязательно для заполнения
        null=True    # Допускается хранение NULL в базе данных
    )
    opening_time = models.TimeField(
        verbose_name="Время открытия",
        blank=True,
        null=True
    )
    closing_time = models.TimeField(
        verbose_name="Время закрытия",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активное расписание (True)",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


#Тренеры
class Trainer(models.Model):
    SPORT_CHOICES = [
        ('Баскетбол', 'Баскетбол'),
        ('Футбол', 'Футбол'),
        ('Волейбол', 'Волейбол'),
        ('Тенис', 'Тенис'),
        ('Бокс', 'Бокс'),
        ('Велоспорт', 'Велоспорт'),
        ('Таэквондо', 'Таэквондо'),
        ('Плавание', 'Плавание'),
        ('Йога', 'Йога'),
    ]
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    email = models.EmailField(verbose_name='Электронная почта')
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=20)
    image = models.ImageField(upload_to='trainers_photos/', blank=True, null=True)
    sport = models.CharField(verbose_name='Спорт', max_length=20, choices=SPORT_CHOICES)
    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'
        ordering = ['email']
    def __str__(self):
        return f'{self.email}'
#Кружки
class Circle(models.Model):
    SPORT_CHOICES = [
        ('Баскетбол', 'Баскетбол'),
        ('Футбол', 'Футбол'),
        ('Волейбол', 'Волейбол'),
        ('Тенис', 'Тенис'),
        ('Бокс', 'Бокс'),
        ('Велоспорт', 'Велоспорт'),
        ('Таэквондо', 'Таэквондо'),
        ('Плавание', 'Плавание'),
        ('Йога', 'Йога'),
    ]
    sports = models.CharField(verbose_name='Виды спорта', max_length=20, choices=SPORT_CHOICES)
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    image = models.ImageField(upload_to='circle_images/',blank=True, null=True)
    image1 = models.ImageField(upload_to='circle_images/',blank=True, null=True)
    image2 = models.ImageField(upload_to='circle_images/',blank=True, null=True)
    image3 = models.ImageField(upload_to='circle_images/',blank=True, null=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, verbose_name='Тренер')
    header1 = models.CharField(verbose_name='Заголовок 1', max_length=255, blank=True)
    description1 = models.TextField(verbose_name='Описание 1', blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=20)
    address = models.CharField(verbose_name='Адрес', max_length=255)
    header2 = models.CharField(verbose_name='Заголовок 2', max_length=255, blank=True)
    description2 = models.TextField(verbose_name='Описание 2', blank=True)
    header3 = models.CharField(verbose_name='Заголовок 3', max_length=255, blank=True)
    description3 = models.TextField(verbose_name='Описание 3', blank=True)
    header4 = models.CharField(verbose_name='Заголовок 4', max_length=255, blank=True)
    description4 = models.TextField(verbose_name='Описание 4', blank=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Кружок'
        verbose_name_plural = 'Кружки'
    def save(self, *args, **kwargs):
        # Эгер pk бар болсо, эскини текшеребиз
        if self.pk:
            try:
                old_circle = Circle.objects.get(pk=self.pk)
                # Эгер жаңы файл жүктөлбөсө, мурунку файлды сактайбыз
                if not self.image:
                    self.image = old_circle.image
                if not self.image1:
                    self.image1 = old_circle.image1
                if not self.image2:
                    self.image2 = old_circle.image2
                if not self.image3:
                    self.image3 = old_circle.image3

                # Башка талааларды да текшерип сактап калууга болот
                if not self.title:
                    self.title = old_circle.title
                if not self.header1:
                    self.header1 = old_circle.header1
                if not self.description1:
                    self.description1 = old_circle.description1
                if not self.phone:
                    self.phone = old_circle.phone
                if not self.address:
                    self.address = old_circle.address
                if not self.header2:
                    self.header2 = old_circle.header2
                if not self.description2:
                    self.description2 = old_circle.description2
                if not self.header3:
                    self.header3 = old_circle.header3
                if not self.description3:
                    self.description3 = old_circle.description3
                if not self.header4:
                    self.header4 = old_circle.header4
                if not self.description4:
                    self.description4 = old_circle.description4
            except ObjectDoesNotExist:
                # Эгер эски рекорд табылбаса, жаңадан түзүү
                pass
        super().save(*args, **kwargs)



class Schedul(models.Model):
    CATEGORY_CHOICES = (
        ('adults', 'Взрослые'),
        ('teens', 'Подростки'),
        ('kids', 'Дети'),
    )

    DAY_OF_WEEK_CHOICES = [
        ('Понедельник', 'Понедельник'),
        ('Вторник', 'Вторник'),
        ('Среда', 'Среда'),
        ('Четверг', 'Четверг'),
        ('Пятница', 'Пятница'),
        ('Суббота', 'Суббота'),
        ('Воскресенье', 'Воскресенье'),
    ]

    circle = models.ForeignKey(Circle, related_name='schedules', on_delete=models.CASCADE, verbose_name="Кружок")
    day_of_week = models.CharField(max_length=12, choices=DAY_OF_WEEK_CHOICES, verbose_name="День недели")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, verbose_name="Категория")
    start_time = models.TimeField(verbose_name="Начало занятия")
    end_time = models.TimeField(verbose_name="Окончание занятия", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активное расписание")

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"

    def __str__(self):
        return f"{self.circle.title} - {self.day_of_week} ({self.start_time} - {self.end_time})"

    @classmethod
    def get_schedules_as_list(cls):
        """Функция для получения всех расписаний в виде списка словарей"""
        schedules = cls.objects.all()
        return [
            {
                'circle': schedule.circle.title,
                'day_of_week': schedule.day_of_week,
                'category': schedule.get_category_display(),
                'start_time': schedule.start_time,
                'end_time': schedule.end_time,
                'is_active': schedule.is_active,
            }
            for schedule in schedules
        ]
#Клиенты
class Client(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Наличные', 'Наличные'),
        ('Карта', 'Карта'),
        ( 'Перевод', 'Перевод'),
    ]
    SPORT_CHOICES = [
        ('Баскетбол', 'Баскетбол'),
        ('Футбол', 'Футбол'),
        ('Волейбол', 'Волейбол'),
        ('Тенис', 'Тенис'),
        ('Бокс', 'Бокс'),
        ('Велоспорт', 'Велоспорт'),
        ('Таэквондо', 'Таэквондо'),
        ('Плавание', 'Плавание'),
        ('Йога', 'Йога'),
    ]
    name = models.CharField(verbose_name='Имя', max_length=255)
    trainer = models.ForeignKey(Trainer, related_name='clients', on_delete=models.CASCADE, verbose_name='Тренер')
    sport = models.CharField(verbose_name='Спорт', max_length=20, choices=SPORT_CHOICES)
    payment_method = models.CharField(verbose_name='Метод оплаты', max_length=10, choices=PAYMENT_METHOD_CHOICES)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Advertisement(models.Model):
    file = models.FileField(upload_to='advertisements/', blank=True, null=True)
    title = models.CharField(max_length=255)
    title1 = models.CharField(max_length=255)
    title2 = models.CharField(max_length=255)
    title3 = models.CharField(max_length=255)
    description = models.TextField(max_length=300)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    site_name = models.CharField(max_length=255)
    site_link = models.URLField()
    installment_plan = models.CharField(max_length=255)
    class Meta:
        verbose_name = "реклама"
        verbose_name_plural = "реклама"
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        # Эгер pk бар болсо, эскини текшеребиз
        if self.pk:
            old_advertisement = Advertisement.objects.get(pk=self.pk)
            # Эгер жаңы файл жүктөлбөсө, мурунку файлды сактайбыз
            if not self.file:
                self.file = old_advertisement.file
            # Башка талааларды да текшерип сактап калууга болот
            if not self.title:
                self.title = old_advertisement.title
            if not self.title1:
                self.title1 = old_advertisement.title1
            if not self.title2:
                self.title2 = old_advertisement.title2
            if not self.title3:
                self.title3 = old_advertisement.title3
            if not self.description:
                self.description = old_advertisement.description
            if not self.phone:
                self.phone = old_advertisement.phone
            if not self.address:
                self.address = old_advertisement.address
            if not self.site_name:
                self.site_name = old_advertisement.site_name
            if not self.site_link:
                self.site_link = old_advertisement.site_link
            if not self.installment_plan:
                self.installment_plan = old_advertisement.installment_plan
        super().save(*args, **kwargs)
#отзыв
class Reviewhall(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveIntegerField(verbose_name="Рейтинг", default=0)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="reviews", verbose_name="Зал")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']


class Reviewcircle(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveIntegerField(verbose_name="Рейтинг", default=0)
    circle = models.ForeignKey(
        'Circle',
        related_name='reviews',  # Измененное related_name
        on_delete=models.CASCADE,
        verbose_name="Кружок"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating}"
class Payment(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    sport = models.CharField(max_length=50, verbose_name="Спорт")
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за месяц")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # Убедитесь, что это поле есть
    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
    def __str__(self):
        return f"{self.name} - {self.sport} - {self.monthly_price} руб."
