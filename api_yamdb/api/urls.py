from django.urls import include, path
from .views import signup, checktoken
from rest_framework import routers
from .views import (
    CategoryViewSet, 
    UserViewSet,
    TitleViewSet,
    GenreViewSet,
    ReviewViewSet)


router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'users', UserViewSet, basename='user')
router.register(r'titles', TitleViewSet, basename='title')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='signups'),
    path('v1/auth/token/', checktoken, name='checktokens')
]
