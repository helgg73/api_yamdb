from rest_framework import serializers
# from django.contrib.auth import get_user_model
# User = get_user_model()
from users.models import User


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email'
        )

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя "me" зарезервировано для служебных целей'
            )
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                f'Пользователь с введенным с логином уже существует'
            )
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с введенным email уже существует'
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
