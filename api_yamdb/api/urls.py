from django.urls import include, path
from .views import signup, checktoken
from rest_framework import routers
from .views import CategoryViewSet


router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name="signups"),
    path('v1/auth/token/', checktoken, name="checktokens")
]
