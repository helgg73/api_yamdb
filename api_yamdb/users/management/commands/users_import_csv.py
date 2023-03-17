import csv
from django.core.management import BaseCommand
from users.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class Command(BaseCommand):
    help = 'Импорт данных из csv файла в БД'

    def handle(self, *args, **options):
        with open('static/data/users.csv') as file:
            validate_object = csv.DictReader(file)
            for row in validate_object:
                try:
                    validate_email(row['email'])
                except ValidationError as error:
                    print("bad email, details:", error)
                else:
                    print("good email")
        with open('static/data/users.csv') as file:
            reader_object = csv.DictReader(file)
            User.objects.bulk_create(User(**data) for data in reader_object)


            # reader_object = csv.reader(file, delimiter=',')
            # line_count = 1
            # for row in reader_object:
            #     if line_count != 1:
            #         try:
            #             user, created = User.objects.get_or_create(
            #                 username=f'{row[1]}',
            #                 email=f'{row[2]}',
            #                 role=f'{row[3]}',
            #                 first_name=f'{row[4]}',
            #                 last_name=f'{row[5]}',
            #             )
            #             print(f'Результат создания пользователя {user}: {created}')
            #         except Exception:
            #             print(f'Данные в строке {line_count} введены не корректно')
            #     line_count += 1
