from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Поля, которые будут отображаться в списке пользователей
    list_display = (
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'birth_date',
        'activation_code',
        'activation_code_created_at',  # Добавляем это поле
        'reset_code',
        'is_active',
        'is_staff'
    )

    # Фильтры для панели
    list_filter = ('is_active', 'is_staff')

    # Разделы для редактирования пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'phone_number', 'birth_date', 'activation_code',
            'activation_code_created_at', 'reset_code')}),  # Исправлено: закрывающая скобка правильно расположена
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)})  # Удаляем 'date_joined' из этого раздела
    )

    # Поля для добавления нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'birth_date'),
        }),
    )

    # По каким полям осуществляется поиск
    search_fields = ('email', 'first_name', 'last_name')

    # Сортировка
    ordering = ('email',)

# Регистрация модели с кастомным админом
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'birth_date', 'gender', 'address')
    search_fields = ('user__username', 'full_name', 'phone')
    list_filter = ('gender',)
    ordering = ('user',)

    fieldsets = (
        (None, {
            'fields': ('user', 'full_name', 'birth_date', 'phone', 'gender', 'address')
        }),
    )