"""Константы"""

# Порт по умолчанию для сетевого ваимодействия
DEFAULT_PORT = 8888
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'

DEFAULT_USER = 'GUEST'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
NON_PRESENCE = 'non_presence'
RESPONSE = 'response'
ERROR = 'error'
QUIT = 'quit'

# Ключи ответов сервера
DICT_ANSWER_CODE = {
    0: 'UNKNOWN',
    100: 'Base notification',
    101: 'Important notification',
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    400: 'Wrong JSON-object/ wrong request',
    401: 'Not authorization',
    402: 'Not authorization',
    403: 'forbidden',
    404: 'Not found',
    409: 'conflict',
    410: 'User offline',
    500: 'Server ERROR',
}

DEBUG = True
LOGGING_LEVEL = 'WARNING'
if DEBUG:
    LOGGING_LEVEL = 'DEBUG'
