from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb import settings
from reviews.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitlesFilter
from .permissions import AdminOnly, AdminOrReadOnly, IsAuthorOrStaffOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReadOnlyTitleSerializer,
                          ReviewSerializer, SignupSerializer, TitlesSerializer,
                          TokenSerializer, UserEditSerializer, UserSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(**serializer.validated_data)
    confirmation_code = default_token_generator.make_token(user)
    email = user.email
    send_mail(
        'Подтверждение регистрации api_yamdb',
        f'Для подтверждение регистрации отправьте {confirmation_code}',
        settings.DEFAULT_PROJECT_EMAIL,
        [f'{email}'],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def checktoken(request, *args, **kwargs):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        message = f'{AccessToken.for_user(user)}'
        return Response(message, status=status.HTTP_200_OK)
    return Response('Не верный код подтверждения',
                    status=status.HTTP_400_BAD_REQUEST)


class Cat_GenryViewSet(mixins.DestroyModelMixin, mixins.ListModelMixin,
                       mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(Cat_GenryViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(Cat_GenryViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    queryset = (
        Title.objects.annotate(rating=Avg('reviews__score')).order_by('name')
    )
    serializer_class = TitlesSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReadOnlyTitleSerializer
        return TitlesSerializer


class UserViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
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


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
