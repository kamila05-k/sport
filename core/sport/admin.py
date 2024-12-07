from django.contrib import admin
from .models import (
    Sport,
    Hall,
    HallInfo,
    HallArena,
    Club,
    ClubAdditionalInfo,
    ClubImage,
    Review,
    HallImage,
    TrainingSchedule,
)

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class HallImageInline(admin.TabularInline):
    model = HallImage
    extra = 1

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('title', 'sport')  # Отображаемые колонки в админке
    search_fields = ('title', 'sport__name')  # Поля для поиска

@admin.register(HallInfo)
class HallInfoAdmin(admin.ModelAdmin):
    list_display = ('hall', 'description')  # Отображаемые поля
    search_fields = ('hall__title', 'description')
    inlines = [HallImageInline]

@admin.register(HallArena)
class HallArenaAdmin(admin.ModelAdmin):
    list_display = ('hall', 'title', 'capacity', 'hourly_rate')  # Отображаемые колонки
    search_fields = ('hall__title', 'title', 'capacity')  # Поля для поиска
    list_filter = ('hall', 'type', 'covering')  # Аналогичная проверка для 'hall'

class ClubImageInline(admin.TabularInline):
    model = ClubImage
    extra = 1

class ClubAdmin(admin.ModelAdmin):
    list_display = ('title', 'sport')
    search_fields = ('title',)
    list_filter = ('sport',)
    inlines = [ClubImageInline]

admin.site.register(Club, ClubAdmin)
@admin.register(ClubAdditionalInfo)
class ClubAdditionalInfoAdmin(admin.ModelAdmin):
    list_display = ('club', 'title', 'title1', 'description1')  # Corrected to use 'description1'
    fields = ('club', 'title', 'title1', 'description1', 'title2', 'description2', 'title3', 'description3', 'video_link', 'address', 'phone')  # Ensure all necessary fields are included
    inlines = [ClubImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'rating', 'created_at', 'sport')
    search_fields = ('user_name', 'text')
    list_filter = ('sport', 'rating',)

@admin.register(TrainingSchedule)
class TrainingScheduleAdmin(admin.ModelAdmin):
    list_display = ('day', 'time', 'sport', 'age_group', 'coach')
    search_fields = ('sport__name', 'coach')
    list_filter = ('day', 'sport',)
