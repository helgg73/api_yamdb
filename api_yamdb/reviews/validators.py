from datetime import datetime
from rest_framework.exceptions import ValidationError

from api_yamdb.config import MIN_SCORE, MAX_SCORE


def score_validator(value):
    if value < MIN_SCORE or value > MAX_SCORE:
        raise ValidationError(f'Оценка должна быть от {MIN_SCORE} до {MAX_SCORE}')
    return value


def year_validator(value):
    now_year = datetime.now().year
    if value > now_year:
        raise ValidationError(f'Год должен быть от 0 до текущего {now_year}')
    return value
