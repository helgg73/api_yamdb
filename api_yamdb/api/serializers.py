from rest_framework import serializers
from titles.models import Titles, Genres, Categories
 

class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Titles
        fields = ('id', 'name', 'yaer', 'description', 'genre', 'category')

class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')

class СategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')
