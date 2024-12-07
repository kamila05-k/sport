from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Номер телефона")
    activation_code = models.CharField(max_length=4, blank=True, null=True)
    activation_code_created_at = models.DateTimeField(null=True, blank=True)  # Время генерации кода
    reset_code = models.CharField(max_length=100, blank=True, null=True)  # Добавьте это поле
    birth_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский')
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField("ФИО", max_length=100, blank=True, null=True)
    birth_date = models.DateField("Дата рождения", blank=True, null=True)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    gender = models.CharField("Пол", max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.CharField("Адрес", max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Профиль пользователя {self.user}"