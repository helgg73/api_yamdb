from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
User = get_user_model()

from .serializers import (
    SignupSerializer,
)


class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(**serializer.validated_data)
        email = user.email
        send_mail(
            'Подтверждение регистрации api_yamdb',
            'Для подтверждение регистрации отправьте код',
            'api_yamdb@api_yamdb.com',
            [f'{email}'],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

