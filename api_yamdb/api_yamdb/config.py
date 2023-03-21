# Параметры пользователей
USERNAME_BLACKLIST = ('me',)
USERNAME_CHARSET = r'[\w.@+-]'

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOISES = (
    (ADMIN, 'Администратор'),
    (USER, 'Аутентифицированный пользователь'),
    (MODERATOR, 'Модератор'),
)

MAX_LENGTH_ROLE = max(ROLE_CHOISES, key = len)
DEFAULT_ROLE = USER

USERNAME_MAX_LENGTH = 150
USER_EMAIL_MAX_LENGTH = 254

# Параметры отзывов
SCORE_CHOICES = (
    (1, '1. Неудовлетворительно'),
    (2, '2. Почти неудовлетворительно'),
    (3, '3. Удовлетворительно'),
    (4, '4. Весьма удовлетворительно'),
    (5, '5. Почти хорошо'),
    (6, '6. Хорошо'),
    (7, '7. Очень хорошо'),
    (8, '8. Почти отлично'),
    (9, '9. Отлично'),
    (10, '10. Превосходно'),)
MIN_SCORE = 1
MAX_SCORE = len(SCORE_CHOICES)
