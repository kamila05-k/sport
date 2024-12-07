from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

# Создаем роутер
router = DefaultRouter()
# Основные URL маршруты
urlpatterns = [
    # зал
    path('halls', HallListCreateView.as_view(), name='hall-list-create'),
    path('halls/<int:pk>', HallRetrieveUpdateDestroyView.as_view(), name='hall-retrieve-update-destroy'),
    path('workschedules', WorkScheduleListCreateView.as_view(), name='workschedule-list-create'),
    path('workschedules/<int:pk>', WorkScheduleRetrieveUpdateDestroyView.as_view(),name='workschedule-retrieve-update-destroy'),
    #Кружки
    path('schedul/', SchedulListCreateView.as_view(), name='schedul-list'),
    path('schedul/<int:pk>/', SchedulRetrieveUpdateDestroyView.as_view(), name='schedul-detail'),
    path('circles/', CircleListCreateView.as_view(), name='circle-list-create'),  # Путь для администратора
    path('circles/<int:pk>/', CircleRetrieveUpdateDestroyView.as_view(), name='circle-retrieve-update-destroy'),  # Путь для администратора с pk
    #login
    path('login/', UserLoginView.as_view(), name='login'),
#Тренеры
    path('trainers/', TrainerCreateView.as_view(), name='trainer-list-create'),
    path('trainers/<int:pk>/', TrainerRetrieveUpdateDestroyView.as_view(), name='trainer-detail'),
#Клиенты
    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroyView.as_view(), name='client-detail'),
    # URL для списка и создания объявлений
    path('advertisements/', AdvertisementListView.as_view(), name='advertisement-list-create'),
    # URL для получения, обновления и удаления одного объявления
    path('advertisements/<int:pk>/', AdvertisementRetrieveUpdateDestroyView.as_view(), name='advertisement-detail'),

    path('reviewshall/', ReviewhallListCreateView.as_view(), name='review-list-create'),

    # URL для получения, обновления и удаления одного отзыва
    path('reviewshall/<int:pk>/', ReviewhallRetrieveUpdateDestroyView.as_view(), name='review-detail'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),

    path('reviewscircle/', ReviewcircleListCreateView.as_view(), name='review_list_create'),  # Список и создание отзывов
    path('reviewscircle/<int:pk>/', ReviewcircleRetrieveUpdateDestroyView.as_view(), name='review_detail'),  # Просмотр, обновление и удаление отзыва

]
# Добавляем маршруты роутера к urlpatterns
urlpatterns += router.urls
