from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_year
from users.models import User
from api_yamdb.settings import (
    MIN_SCORE, MAX_SCORE, ERROR_SCORE_MESSAGE,
    MAX_LENGTH_TITLE_SUBSECTION_NAME, MAX_LENGTH_TITLE_SUBSECTION_SLUG,
    MAX_LENGTH_TITLE_NAME, SLICE_TEXT_FOR_STR
)


class CaterogyGenreBase(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_TITLE_SUBSECTION_NAME,
        db_index=True)
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=MAX_LENGTH_TITLE_SUBSECTION_SLUG,
        unique=True)

    class Meta:
        ordering = ('name',)
        abstract = True

    def __str__(self):
        return self.name


class Category(CaterogyGenreBase):

    class Meta(CaterogyGenreBase.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CaterogyGenreBase):

    class Meta(CaterogyGenreBase.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_TITLE_NAME,
        db_index=True)
    description = models.TextField(
        verbose_name='Описание',
        null=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        through_fields=('title', 'genre'),
        verbose_name='Жанр',)
    year = models.IntegerField(
        verbose_name='Дата выпуска',
        db_index=True,
        validators=(validate_year,))

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)


class ReviewCommentBase(models.Model):
    text = models.TextField(
        verbose_name='Текст')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
        abstract = True

    def __str__(self):
        return self.text[:SLICE_TEXT_FOR_STR]


class Review(ReviewCommentBase):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    score = models.SmallIntegerField(
        'Оценка произведения',
        validators=(
            MaxValueValidator(MAX_SCORE, message=ERROR_SCORE_MESSAGE),
            MinValueValidator(MIN_SCORE, message=ERROR_SCORE_MESSAGE))
    )

    class Meta(ReviewCommentBase.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'), name='unique_review'
            ),
        ]


class Comment(ReviewCommentBase):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE)

    class Meta(ReviewCommentBase.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментрий к отзывы'
        verbose_name_plural = 'Комментарии к отзыву'
