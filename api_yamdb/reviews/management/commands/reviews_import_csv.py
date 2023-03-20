import csv
from django.core.management import BaseCommand
from reviews.models import (
    Category,
    Genre,
    Title,
    Comment,
    Review,
    GenreTitle,
)


FILES = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    GenreTitle: 'genre_title.csv',
}


class Command(BaseCommand):
    help = 'Импорт данных из csv файлов в БД'

    def handle(self, *args, **options):
        for model, file_csv in FILES.items():
            with open(f'static/data/{file_csv}') as file:
                reader_object = csv.DictReader(file)
                model.objects.bulk_create(
                    model(**data) for data in reader_object
                )
