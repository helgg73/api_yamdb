import csv
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Импорт данных из csv файла в БД'

    def handle(self, *args, **options):
        with open('static/data/users.csv') as file:
            reader_object = csv.reader(file, delimiter=',')
            line_count = 0
            for row in reader_object:
                if line_count != 0:
                    try:
                        user, created = User.objects.get_or_create(
                            username=f'{row[1]}',
                            email=f'{row[2]}',
                            role=f'{row[3]}',
                            first_name=f'{row[4]}',
                            last_name=f'{row[5]}',
                        )
                    except Exception:
                        print('Данные в строке введены не корректно')
                    print(f'{user} создан: {created}')
                line_count += 1
