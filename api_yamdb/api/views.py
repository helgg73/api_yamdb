from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from .serializers import (
    SignupSerializer,
    TokenSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, created = User.objects.get_or_create(**serializer.validated_data)
    confirmation_code = default_token_generator.make_token(user)
    email = user.email
    print(confirmation_code)
    send_mail(
        'Подтверждение регистрации api_yamdb',
        f'Для подтверждение регистрации отправьте {confirmation_code}',
        'api_yamdb@api_yamdb.com',
        [f'{email}'],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_tokens_for_user(user):
    access_token = AccessToken.for_user(user)

    return access_token


@api_view(['POST'])
@permission_classes([AllowAny])
def checktoken(request, *args, **kwargs):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        message = f'{get_tokens_for_user(user)}'
        return Response(message, status=status.HTTP_200_OK)
    return Response('Не верный код подтверждения', status=status.HTTP_400_BAD_REQUEST)
