from django.urls import path
from .views import *
urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user-registration'),
    path('activate/', ActivationAPIView.as_view(), name='activate'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('advertise/message/', RegistrationMessageAPIView.as_view(), name='registration-message'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password-verify/', ResetPasswordVerifyView.as_view(), name='reset_password_verify'),
    path('resend-activation-code/', ResendActivationCodeView.as_view(), name='resend_activation_code'),
    path('resen-password-verify-code/', ResenActivationCodeView.as_view(), name='resend_activation_code'),
    path('profile/<int:pk>/', ProfileRetrieveUpdateView.as_view(), name='profile-detail'),

]
