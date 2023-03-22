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

MAX_LENGTH_ROLE = 20
DEFAULT_ROLE = USER

USERNAME_MAX_LENGTH = 150
USER_EMAIL_MAX_LENGTH = 254

# Параметры произведений

MAX_LENGTH_TITLE_SUBSECTION_NAME = 256
MAX_LENGTH_TITLE_SUBSECTION_SLUG = 50
MAX_LENGTH_TITLE_NAME = 256

# Параметры отзывов
MIN_SCORE = 1
MAX_SCORE = 10
ERROR_SCORE_MESSAGE = f'Оценка должна быть от {MIN_SCORE} до {MAX_SCORE}'

DEFAULT_PROJECT_EMAIL = 'api_yamdb@api_yamdb.com'
