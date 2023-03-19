from django.db import models
from users.models import User
from reviews.validators import score_validator
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

SCORE_CHOICES = (
    (1, '1. Неудовлетворительно'),
    (2, '2. Почти неудовлетворительно'),
    (3, '3. Удовлетворительно'),
    (4, '4. Весьма удовлетворительно'),
    (5, '5. Почти хорошо'),
    (6, '6. Хорошо'),
    (7, '7. Очень хорошо'),
    (8, '8. Почти отлично'),
    (9, '9. Отлично'),
    (10, '10. Превосходно'),)


class Category(models.Model):
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


class Genre(models.Model):
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


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        db_index=True)
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
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


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    text = models.TextField(
        verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE)
    score = models.SmallIntegerField(
        choices=SCORE_CHOICES,
        validators=(score_validator,),
        verbose_name='Оценка произведения',
        )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        default_related_name = "reviews"
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=("title", "author"), name="unique_review"
            ),
        ]


class Сomment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE)
    text = models.TextField(
        verbose_name='Текст комментария',
        null=True)
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        default_related_name = "comments"
        verbose_name = 'Комментрий к отзывы'
        verbose_name_plural = 'Комментарии к отзыву'
        ordering = ['pub_date']
