from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from datetime import datetime

class Сategories(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(verbose_name='Слаг', max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    

class Genres(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(verbose_name='Слаг', max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']
    
    
class Titles(models.Model):
    name =  models.CharField(verbose_name='Название', max_length=200)
    description = models.TextField(null=True, blank=True)

    category = models.ForeignKey(Сategories, on_delete = models.SET_NULL, null = True,
        related_name='category')
    genre = models.ForeignKey(Genres, on_delete = models.SET_NULL, null = True,
        related_name='genre')
    year = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(datetime.now().year)])

    def __str__(self):
        return self.name
    
    
