"""

Программа сервера

"""
import json
import logging
from socket import AF_INET, SOCK_STREAM, socket
from utils.utils import create_parser
from utils.config import ENCODING, MAX_CONNECTIONS, MAX_PACKAGE_LENGTH
from log import server_log_config

RESPONSE_ERROR = 400
RESPONSE_OK = 200

SERVER_LOGGER = logging.getLogger('server')


class Server:
    def __init__(self, logger):
        self.logger = logger
        self._s = socket(AF_INET, SOCK_STREAM)
        self.addr, self.port = create_parser()
        self.logger.info(f'Сервер создан с параметрами {self.addr} {self.port}')

    def create_connection(self):
        try:
            self._s.bind((self.addr, self.port))
            self._s.listen(MAX_CONNECTIONS)
            self.logger.info(f'Сервер подключен')
        except:
            self.logger.critical(f'Сервер не подключен')

        while True:
            client, client_address = self._s.accept()
            response = RESPONSE_ERROR
            try:
                data = client.recv(MAX_PACKAGE_LENGTH)
                if data:
                    json_answer = data.decode(ENCODING)
                    response = self.process_client_message(json.loads(json_answer))
            except:
                self.logger.error(f'Принято некорректное сообщение от клиента')
            finally:
                client.send(f'{response}'.encode(ENCODING))
                client.close()

    def process_client_message(self, message):
        self.logger.info(f'Обработка сообщения {message}')
        if message['action'] == 'presence' and message['user']['account_name'] == 'GUEST':
            return RESPONSE_OK
        return RESPONSE_ERROR


def main():
    server = Server(SERVER_LOGGER)
    server.create_connection()


if __name__ == '__main__':
    main()
