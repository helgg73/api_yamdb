import csv

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Импорт данных из csv файла users.csv в БД'

    def handle(self, *args, **options):
        with open('static/data/users.csv') as file:
            reader_object = csv.DictReader(file)
            User.objects.bulk_create(User(**data) for data in reader_object)
