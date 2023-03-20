from rest_framework.exceptions import ValidationError


def score_validator(value):
    if value < 0 or value > 10:
        raise ValidationError('Оценка должна быть от 0 до 10')
    return value
