import re

from rest_framework.exceptions import ValidationError

from api_yamdb.config import USERNAME_BLACKLIST, USERNAME_CHARSET


def validate_username(username):
    if username.lower() in USERNAME_BLACKLIST:
        raise ValidationError('Имя пользователя не разрешено')
    forbidden = re.sub(USERNAME_CHARSET, '', username)
    if forbidden != '':
        raise ValidationError(
            f'Имя пользователя не должно содержать {set(forbidden)}'
        )
    return username
