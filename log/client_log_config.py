import os
import logging
from datetime import datetime

from utils.config import LOGGING_LEVEL

LOG = logging.getLogger('client')

FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

LOG_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(LOG_PATH, 'logs/client.log')

LOG_FILE = logging.FileHandler(LOG_PATH, encoding='utf8')
LOG_FILE.setFormatter(FORMATTER)

LOG.addHandler(LOG_FILE)
LOG.setLevel(LOGGING_LEVEL)

LOG.info(f'Лог-файл от {datetime.today()}')

# отладка
if __name__ == '__main__':
    LOG.critical('ОТЛАДКА Критическая ошибка')
    LOG.error('ОТЛАДКА Ошибка')
    LOG.debug('ОТЛАДКА Отладочная информация')
    LOG.info('ОТЛАДКА Информационное сообщение')