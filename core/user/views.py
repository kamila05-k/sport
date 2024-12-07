import random
import string
import re
import logging
from django.core.mail import BadHeaderError
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404, RetrieveUpdateAPIView
from rest_framework.views import APIView
from datetime import timedelta
from django.utils import timezone
from .models import *
from .serializers import *

logger = logging.getLogger(__name__)

def generate_activation_code():
    """Генерирует случайный код активации, состоящий только из цифр, длиной 4 символа."""
    return ''.join(random.choices(string.digits, k=4))

def validate_password(password):
    """Проверка пароля на минимум 5 символов, максимум 10, наличие заглавной буквы, цифры и строчной буквы."""
    if len(password) < 5 or len(password) > 10:
        return False, _('Пароль должен быть от 5 до 10 символов.')
    if not re.search(r'[A-Z]', password):
        return False, _('Пароль должен содержать хотя бы одну заглавную букву.')
    if not re.search(r'[a-z]', password):
        return False, _('Пароль должен содержать хотя бы одну строчную букву.')
    if not re.search(r'[0-9]', password):
        return False, _('Пароль должен содержать хотя бы одну цифру.')
    return True, ''

class RegistrationAPIView(generics.CreateAPIView):
    """Регистрация нового пользователя."""
    serializer_class = UserRegistrationSerializer
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logger.debug(f"Registration request data: {request.data}")
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return Response({
                'response': False,
                'message': _('Ошибка валидации')
            }, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')
        is_valid, message = validate_password(password)
        if not is_valid:
            return Response({
                'response': False,
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = serializer.save()
            user.is_active = False
            user.set_password(password)
            user.save()

            # Генерация и установка кода активации
            activation_code = generate_activation_code()
            user.activation_code = activation_code
            user.activation_code_created_at = timezone.now()  # Сохранение времени создания кода активации
            user.save()

            # Формирование сообщения на русском языке
            message_ru = (
                f"<h1>{_('Здравствуйте')}, {user.email}!</h1>"
                f"<p>{_('Поздравляем Вас с успешной регистрацией на сайте')} {settings.BASE_URL}</p>"
                f"<p>{_('Ваш код активации')}: {activation_code}</p>"
                f"<p>{_('С наилучшими пожеланиями')},<br>{_('Команда')} {settings.BASE_URL}</p>"
            )

            # Отправка письма
            email_subject = _('Активация вашего аккаунта')

            try:
                send_mail(
                    email_subject,
                    '',  # Пустое текстовое сообщение, т.к. используем html_message
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                    html_message=message_ru,
                )
                logger.debug(f"Activation email sent to {user.email}")
            except Exception as e:
                logger.error(f"Error sending activation email: {str(e)}")
                return Response({
                    'response': False,
                    'message': _('Не удалось отправить письмо с кодом активации.')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                'response': True,
                'message': _(
                    'Пользователь успешно зарегистрирован. Проверьте вашу электронную почту для получения кода активации.')
            }, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            logger.error(f"IntegrityError: {str(e)}")
            if 'email' in str(e):
                return Response({
                    'response': False,
                    'message': _('Такой email уже зарегистрирован.')
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'response': False,
                'message': _('Не удалось зарегистрировать пользователя.')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ActivationAPIView(generics.GenericAPIView):
    serializer_class = ActivationCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Сериализатор невалиден: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        activation_code = serializer.validated_data.get('activation_code')
        try:
            user = get_object_or_404(CustomUser, activation_code=activation_code)

            # Проверка срока действия кода (1 час)
            if user.activation_code_created_at and timezone.now() > user.activation_code_created_at + timedelta(hours=1):
                return Response({
                    'response': False,
                    'message': _('Срок действия кода активации истек.')
                }, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.activation_code = ''
            user.activation_code_created_at = None
            user.save()

            return Response({
                'response': True,
                'message': _('Ваш аккаунт успешно активирован.')
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Ошибка активации: {str(e)}")
            return Response({
                'response': False,
                'message': _('Ошибка активации.')
            }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.CreateAPIView):
    """Аутентификация пользователя."""
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')

        if user is None:
            return Response({
                'response': False,
                'message': _('Неверный логин или пароль.')
            }, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'response': True,
            'token': token.key
        }, status=status.HTTP_200_OK)

class RegistrationMessageAPIView(APIView):
    """Возвращает сообщение о необходимости регистрации для размещения рекламы."""

    def get(self, request, *args, **kwargs):
        serializer = RegistrationMessageSerializer(
            data={'message': 'Для размещения рекламы сначала зарегистрируйтесь.'})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    """Запрос на сброс пароля."""
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
            reset_code = generate_activation_code()
            user.reset_code = reset_code
            user.reset_code_created_at = timezone.now()  # Сохранение времени создания кода сброса
            user.save()

            message = (
                f"Здравствуйте, {user.email}!\n\n"
                f"<p>{_('Ваш код для восстановления пароля')}: {reset_code}</p>"
                f"<p>{_('С наилучшими пожеланиями')},<br>{_('Команда')} {settings.BASE_URL}</p>"
            )
            send_mail(
                _('Восстановление пароля'),
                '',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=message,
            )
            return Response({
                'response': True,
                'message': _('Письмо с инструкциями по восстановлению пароля было отправлено на ваш email.')
            })

        except CustomUser.DoesNotExist:
            return Response({
                'response': False,
                'message': _('Пользователь с этим адресом электронной почты не найден.')
            }, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordVerifyView(generics.GenericAPIView):
    """Подтверждение сброса пароля."""
    serializer_class = ResetPasswordVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_code = serializer.validated_data['reset_code']

        try:
            # Проверяем, существует ли пользователь с данным кодом сброса
            user = CustomUser.objects.get(reset_code=reset_code)

            # Сброс пароля
            user.reset_code = ''  # Очищаем код сброса после подтверждения
            user.reset_code_created_at = None  # Очищаем дату создания кода
            user.save()

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'response': True,
                'message': _('Пароль успешно сброшен. Теперь вы можете войти с новым паролем.'),
            }, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            logger.error(f"User with reset_code {reset_code} does not exist.")
            return Response({
                'response': False,
                'message': _('Неверный код для сброса пароля.')
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error in ResetPasswordVerifyView: {str(e)}")
            return Response({
                'response': False,
                'message': _('Произошла ошибка при сбросе пароля.')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResendActivationCodeView(generics.GenericAPIView):
    """Повторная отправка кода активации на email."""
    serializer_class = ResendActivationCodeSerializer
    parser_classes = [JSONParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
            # Генерация нового кода активации
            activation_code = generate_activation_code()
            user.activation_code = activation_code
            user.activation_code_created_at = timezone.now()
            user.save()

            message = (
                f"Здравствуйте, {user.email}!\n\n"
                f"<p>{_('Ваш новый код активации')}: {activation_code}</p>"
                f"<p>{_('С наилучшими пожеланиями')},<br>{_('Команда')} {settings.BASE_URL}</p>"
            )

            try:
                send_mail(
                    _('Активация вашего аккаунта'),
                    '',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                    html_message=message,
                )
            except BadHeaderError:
                return Response({
                    'response': False,
                    'message': _('Ошибка при отправке письма. Попробуйте еще раз позже.')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                'response': True,
                'message': _('Новый код активации был отправлен на ваш email.')
            })

        except CustomUser.DoesNotExist:
            return Response({
                'response': False,
                'message': _('Пользователь с этим адресом электронной почты не найден.')
            }, status=status.HTTP_404_NOT_FOUND)

class ResenActivationCodeView(generics.GenericAPIView):
    """Повторная отправка кода активации на email."""
    serializer_class = ResendActivationCodeSerializer
    parser_classes = [JSONParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
            # Генерация нового кода восстановления пароля
            reset_code = generate_activation_code()  # Изменено на reset_code
            user.reset_code = reset_code
            user.reset_code_created_at = timezone.now()
            user.save()

            message = (
                f"Здравствуйте, {user.email}!\n\n"
                f"<p>{_('Ваш код для восстановления пароля')}: {reset_code}</p>"  # Сообщение для восстановления пароля
                f"<p>{_('С наилучшими пожеланиями')},<br>{_('Команда')} {settings.BASE_URL}</p>"
            )

            try:
                send_mail(
                    _('Восстановление пароля'),
                    '',  # Пустое тело, так как мы используем html_message
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                    html_message=message,
                )

            except BadHeaderError:
                return Response({
                    'response': False,
                    'message': _('Ошибка при отправке письма. Попробуйте еще раз позже.')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                'response': True,
                'message': _('Новый код для восстановления пароля был отправлен на ваш email.')
            })

        except CustomUser.DoesNotExist:
            return Response({
                'response': False,
                'message': _('Пользователь с этим адресом электронной почты не найден.')
            }, status=status.HTTP_404_NOT_FOUND)


class ProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
