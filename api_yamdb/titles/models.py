from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


class Categories(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        db_index=True)
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=50,
        unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Genres(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        db_index=True)
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=50,
        unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Titles(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        db_index=True)
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True)
    category = models.ForeignKey(
        Categories,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True)
    genre = models.ManyToManyField(
        Genres,
        verbose_name='Жанр',
        db_index=True)
    year = models.IntegerField(
        verbose_name='Дата выпуска',
        db_index=True,
        validators=[MinValueValidator(0),
                    MaxValueValidator(datetime.now().year)])

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = "titles"
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']
