from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, check_confirmation_code,
                    signup)

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'users', UserViewSet, basename='user')
router.register(r'titles', TitleViewSet, basename='title')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)

auth_path = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', check_confirmation_code, name='check_confirmation_code')

]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(auth_path)),
]
