from django.urls import path
from .views import signup


urlpatterns = [
    path('v1/auth/signup/', signup, name="signup")

]
