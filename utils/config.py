"""Константы"""

# Порт по умолчанию для сетевого ваимодействия
import json
import time

DEFAULT_PORT = 8888
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'

DEFAULT_CLIENT_ID = 'UNKNOWN'

DEFAULT_USER = 'GUEST'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'

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

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'

# Ключ для всех клиентов
ALL_CLIENTS = 'all'
SERVER_ONLY = 'server'


def get_message(sender, message_text, destination):
    return {
        ACTION: MESSAGE,
        SENDER: sender,
        DESTINATION: destination,
        TIME: time.time(),
        MESSAGE_TEXT: message_text
    }


def dict_to_bytes(the_dict):
    return json.dumps(the_dict, indent=2).encode(ENCODING)


def bytes_to_dict(the_binary):
    return json.loads(the_binary.decode(ENCODING))


DEBUG = True
LOGGING_LEVEL = 'WARNING'
if DEBUG:
    LOGGING_LEVEL = 'DEBUG'
