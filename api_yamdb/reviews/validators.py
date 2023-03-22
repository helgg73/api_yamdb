from django.utils import timezone
from rest_framework.exceptions import ValidationError


def validate_year(year):
    now_year = timezone.now().year
    if year > now_year:
        raise ValidationError(
            f'Год должен быть не больше текущего года: {now_year}'
        )
    return year
