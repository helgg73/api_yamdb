from datetime import datetime
from rest_framework.exceptions import ValidationError


def score_validator(value):
    if value < 1 or value > 10:
        raise ValidationError('Оценка должна быть от 1 до 10')
    return value

def year_validator(value):
    if value < 0 or value > datetime.now().year:
        raise ValidationError('Год должен быть от 0 до текущего')
    return value