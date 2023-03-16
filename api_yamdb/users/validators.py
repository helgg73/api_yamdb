import re

from rest_framework.exceptions import ValidationError


def username_validator(value):
    forbidden = re.sub(r'[\w.@+-]', '', value)
    if value == "me":
        raise ValidationError('Имя пользователя "me" не разрешено')
    elif forbidden != '':
        raise ValidationError(
            f"Имя пользователя не должно содержать {forbidden}"
        )
    return value
