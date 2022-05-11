from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .serializers import UserSerializer


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


@api_view(['POST'])
def signup(request):
    """Регистрация пользователя и отправка кода подтверждения на его email."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        token_generator = PasswordResetTokenGenerator()
        user = get_user_model().objects.get(
            username=serializer.initial_data['username'])
        confirmation_code = token_generator.make_token(user=user)
        user.confirmation_code = confirmation_code
        user.save()
        try:
            send_code(user.email, user.confirmation_code)
        except:
            print("Ошибка отпрравки email с кодом подтверждения")
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
