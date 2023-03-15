from django.urls import path
from .views import signup, checktoken


urlpatterns = [
    path('v1/auth/signup/', signup, name="signups"),
    path('v1/auth/token/', checktoken, name="checktokens")
]

