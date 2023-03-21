from django.utils import timezone
from rest_framework.exceptions import ValidationError

from api_yamdb.config import MIN_SCORE, MAX_SCORE


def validate_year(year):
    now_year = timezone.now().year
    if year > now_year:
        raise ValidationError(f'Год должен быть от 0 до текущего {now_year}')
    return year
