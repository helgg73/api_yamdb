from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import User
from titles.models import Categories, Titles, Genres
from users.validators import username_validator
from reviews.models import Reviews
from reviews.validators import score_validator


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(username_validator,),
    )
    email = serializers.EmailField(
        max_length=254,
        allow_blank=False)

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



class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategoriesSerializer()

    class Meta:
        model = Titles
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Categories.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    score = serializers.IntegerField(
        validators=(score_validator,)
    )

    class Meta:
        fields = '__all__'
        model = Reviews
        validators = (
            UniqueTogetherValidator(
                queryset=Reviews.objects.all(),
                message = 'Можно оставить только один отзыв',
                fields=('author', 'title')
            ),
        )