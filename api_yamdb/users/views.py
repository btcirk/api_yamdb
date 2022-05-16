from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from .serializers import UserSerializer, TokenSerializer

User = get_user_model()


def send_code(recipient, confirmation_code):
    """Отправка кода подтверждения на email пользователя."""
    status = send_mail(
        'Код подтверждения',
        f'Здравствуйте, используйте этот код подтверждения '
        f'{confirmation_code} для получения токена.',
        'noreply@yamdb.com',
        [f'{recipient}'],
        fail_silently=False,
    )
    return status


def get_tokens_for_user(user):
    """Генерация токена для доступа к API."""
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token)
    }


@api_view(['POST'])
def signup(request):
    """Регистрация пользователя и отправка кода подтверждения на его email."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        token_generator = PasswordResetTokenGenerator()
        user = User.objects.get(
            username=serializer.initial_data['username'])
        confirmation_code = token_generator.make_token(user=user)
        user.confirmation_code = confirmation_code
        user.save()
        try:
            send_code(user.email, user.confirmation_code)
        except Exception:
            print("Ошибка отправки email с кодом подтверждения")
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def token(request):
    """Получение JWT-токена в обмен на username и confirmation_code."""
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.initial_data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.initial_data['confirmation_code']
        if user.confirmation_code == confirmation_code:
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response('Неверный confirmation_code',
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
