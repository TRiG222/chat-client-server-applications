"""

Программа клиента.

"""
import os
import sys
import threading
import socket
from utils.utils import create_arguments_parser
from utils.config import MAX_PACKAGE_LENGTH, get_message, dict_to_bytes, bytes_to_dict, ALL_CLIENTS, PRESENCE, \
    SERVER_ONLY
from utils.decorators import log
import logging
from log import client_log_config

CLIENT_LOGGER = logging.getLogger('client')

# class Client:
#     def __init__(self, logger):
#         self.addr, self.port, self.client_id = create_arguments_parser()
#         self.logger = logger
#         self._s = socket(AF_INET, SOCK_STREAM)
#
#         self.logger.info(f'Клиент {self.client_id} создан с параметрами {self.addr} {self.port}')
#
#     @log
#     def create_connection(self):
#         try:
#             self._s.connect((self.addr, self.port))
#             self.logger.info(f'Клиент подключен с параметрами {self.addr} {self.port}')
#             self.send(PresenceMessage(user={'account_name': self.client_id}))
#         except Exception as e:
#             self.logger.critical(f'Не удалось подключиться к серверу {e}')
#             print('Не удалось подключиться к серверу')
#             exit(1)
#
#     @log
#     def send(self, message):
#         print('send >>>', message)
#         self.logger.info(f'Отправка сообщения {message.action} от клиента {self.client_id}')
#
#         try:
#             self._s.send(message.to_bytes())
#             self.logger.info(f'Сообщение {message.action} от клиента {self.client_id} отправлено на сервер')
#         except Exception as e:
#             self.logger.error(f'send> {e}')
#
#         return self.get_response()
#
#     @log
#     def get_response(self):
#         data = self._s.recv(MAX_PACKAGE_LENGTH)
#         response = data.decode(ENCODING)
#         print('get_response >>>', response)
#         self.logger.info(f'Получен ответ {response} от сервера для клиента {self.client_id}')
#         return response
#
#     @log
#     def send_chat_message(self, text):
#         print('send_chat_message', text)
#         self.send(ChatMessage(text=text, user={'account_name': self.client_id}))
#
#
#
#
# if __name__ == '__main__':
#     client = Client(CLIENT_LOGGER)
#     client.create_connection()
#     client.send_chat_message(f'client {client.client_id}')

"""
"""


def close(client):
    """
    Выходим из чата
    """
    send_message(client, '{} отключился'.format(client.client_name), ALL_CLIENTS)
    client.sock.close()
    os._exit(0)


def send_message(client, message, to):
    """
    Отправляем сообщение
    """

    formatted = get_message(client.client_name, message, to)
    client.sock.sendall(dict_to_bytes(formatted))


class Send(threading.Thread):
    def __init__(self, sock, client_name):
        super().__init__()
        self.sock = sock
        self.client_name = client_name

    def run(self):
        while True:
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]
            if message == 'EXIT':
                break
            else:
                send_message(self, '{}: {}'.format(self.client_name, message), ALL_CLIENTS)

        close(self)


class Receive(threading.Thread):
    def __init__(self, sock, client_name, messages):
        super().__init__()
        self.sock = sock
        self.client_name = client_name
        self.messages = messages

    def run(self):
        while True:
            message = self.sock.recv(MAX_PACKAGE_LENGTH)
            if message:
                if self.messages:
                    msg = bytes_to_dict(message)
                    print('Получено сообщение {}'.format(msg))
            else:
                print(self.messages, 'Потеряно соединение с сервером')
                close(self)


class Client:
    def __init__(self, host, port, client_name, messages):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_name = client_name
        self.messages = messages

    def start(self):
        print(self.messages, 'Подключаемся к {}:{}'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        send = Send(self.sock, self.client_name)
        receive = Receive(self.sock, self.client_name, self.messages)
        send.start()
        receive.start()
        send_message(self, PRESENCE, SERVER_ONLY)
        print(self.messages, 'Подключились!')
        return receive

    def send(self, text_input, to_input):
        message = text_input
        to = to_input

        if message == 'EXIT':
            close(self)
        else:
            print(self.messages, 'Вы > {}: {}'.format(to, message))
            send_message(self, message, to)


def main(host, port, client_name):
    messages = client_name
    client = Client(host, port, client_name, messages)
    receive = client.start()
    while True:
        client.send(input('text_input'), input('to_input'))


if __name__ == '__main__':
    args = create_arguments_parser()
    main(args[0], args[1], args[2])
