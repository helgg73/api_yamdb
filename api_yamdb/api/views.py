from rest_framework import viewsets, status
from rest_framework.response import Response
# from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth import get_user_model
User = get_user_model()

from .serializers import (
    SignupSerializer,
)


class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer


