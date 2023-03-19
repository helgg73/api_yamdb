from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from .serializers import (
    SignupSerializer,
    TokenSerializer,
    CategorySerializer,
    GenreSerializer,
    TitlesSerializer,
    UserSerializer,
    UserEditSerializer,
    ReadOnlyTitleSerializer,
    ReviewSerializer
)
from rest_framework import viewsets, filters, mixins

from reviews.models import Review, Category, Title, Genre
from .permissions import AdminOrReadOnly, AdminOnly, IsAuthorOrStaffOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from .filters import TitlesFilter

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        return Response('Неверное сочетание имени и email',
                        status.HTTP_400_BAD_REQUEST)
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
    return Response('Не верный код подтверждения',
                    status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(mixins.DestroyModelMixin, mixins.ListModelMixin,
                      mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.DestroyModelMixin, mixins.ListModelMixin,
                   mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitlesSerializer



class UserViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    permission_classes = (AdminOnly,)

    @action(
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrStaffOrReadOnly,)
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
