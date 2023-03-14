from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignupViewSet

router = DefaultRouter()
router.register('auth/signup', SignupViewSet, basename='signups')


urlpatterns = [
    path('v1/', include(router.urls)),
]

