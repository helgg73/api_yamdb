from rest_framework import serializers

from users.models import User
from titles.models import Categories
from users.validators import username_validator


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(username_validator,),
    )
    email = serializers.EmailField(
        max_length=254,
        allow_blank=False
        )

    class Meta:
        model = User
        fields = (
            'username', 'email'
        )


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


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')
        lookup_field = 'slug'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User

    def validate_username(self, value):
        return username_validator(value)


class UserEditSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)
