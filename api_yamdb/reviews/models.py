from django.db import models
from users.models import User
from titles.models import Titles

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


class Reviews(models.Model):
    title = models.ForeignKey(
        Titles,
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
        verbose_name='Оценка произведения')
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


class Сomments(models.Model):
    reviews = models.ForeignKey(
        Reviews,
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
