import logging.handlers
import logging
import os

from utils.config import LOGGING_LEVEL

LOG = logging.getLogger('server')

LOG_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(LOG_PATH, 'logs/server.log')

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

LOG_FILE = logging.handlers.TimedRotatingFileHandler(LOG_PATH, encoding='utf8', interval=1, when='D')
LOG_FILE.setFormatter(FORMATTER)

LOG_FILE.setLevel(LOGGING_LEVEL)
LOG.addHandler(LOG_FILE)
LOG.setLevel(LOGGING_LEVEL)



# отладка
if __name__ == '__main__':
    LOG.critical('ОТЛАДКА Критическая ошибка')
    LOG.error('ОТЛАДКА Ошибка')
    LOG.debug('ОТЛАДКА Отладочная информация')
    LOG.info('ОТЛАДКА Информационное сообщение')