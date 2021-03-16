"""

Программа клиента.

"""

from socket import AF_INET, SOCK_STREAM, socket
from utils.utils import ChatMessage, create_arguments_parser, PresenceMessage
from utils.config import ENCODING, MAX_PACKAGE_LENGTH
from utils.decorators import log
import logging
from log import client_log_config

CLIENT_LOGGER = logging.getLogger('client')


class Client:
    def __init__(self, logger):
        self.addr, self.port, self.client_id = create_arguments_parser()
        # self.account_name = user
        self.logger = logger
        # self.addr, self.port = create_arguments_parser()
        self._s = socket(AF_INET, SOCK_STREAM)

        self.logger.info(f'Клиент {self.client_id} создан с параметрами {self.addr} {self.port}')

    @log
    def create_connection(self):
        try:
            self._s.connect((self.addr, self.port))
            self.logger.info(f'Клиент подключен с параметрами {self.addr} {self.port}')
            self.send(PresenceMessage(user={'account_name': self.client_id}))
        except Exception as e:
            self.logger.critical(f'Не удалось подключиться к серверу {e}')
            print('Не удалось подключиться к серверу')
            exit(1)

    @log
    def send(self, message):
        print('send >>>', message)
        self.logger.info(f'Отправка сообщения {message.action} от клиента {self.client_id}')

        try:
            self._s.send(message.to_bytes())
            self.logger.info(f'Сообщение {message.action} от клиента {self.client_id} отправлено на сервер')
        except Exception as e:
            self.logger.error(f'send> {e}')

        return self.get_response()

    @log
    def get_response(self):
        data = self._s.recv(MAX_PACKAGE_LENGTH)
        response = data.decode(ENCODING)
        print('get_response >>>', response)
        self.logger.info(f'Получен ответ {response} от сервера для клиента {self.client_id}')
        return response

    @log
    def send_chat_message(self, text):
        print('send_chat_message', text)
        self.send(ChatMessage(text=text, user={'account_name': self.client_id}))

    # @log
    # def close_connection(self):
    #     self.send_message(NonPresenceMessage(user={'account_name': self.account_name}))
    # @log
    # def send_message(self, message):
    #     self.logger.info(f'Отправка сообщения {message.action} от клиента {self.account_name}')
    #     try:
    #         self._s.send(message.to_bytes())
    #         print('send', message, message.to_bytes())
    #         self.logger.info(f'Сообщение {message.action} от клиента {self.account_name} отправлено на сервер')
    #     except:
    #         self.logger.error(f'Сообщение {message.action} от клиента {self.account_name} не отправлено на сервер')
    #
    #     return self.get_response()
    # @log
    # def get_response(self):
    #     response = Response(self._s.recv(MAX_PACKAGE_LENGTH).decode(ENCODING))
    #     self.logger.info(f'Получен ответ {response} от сервера для клиента {self.account_name}')
    #     print('response >>>', response)
    #     return response


if __name__ == '__main__':
    client = Client(CLIENT_LOGGER)
    client.create_connection()
    client.send_chat_message(f'client {client.client_id}')
