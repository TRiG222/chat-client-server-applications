"""

Программа сервера

"""
import json
import logging
from socket import AF_INET, SOCK_STREAM, socket
from utils.utils import create_arguments_parser
from utils.config import ENCODING, MAX_CONNECTIONS, MAX_PACKAGE_LENGTH
from log import server_log_config
from utils.decorators import log
import select


RESPONSE_ERROR = 400
RESPONSE_OK = 200

SERVER_LOGGER = logging.getLogger('server')


class Server:
    def __init__(self, logger):
        self.logger = logger
        self._s = socket(AF_INET, SOCK_STREAM)
        self.addr, self.port, self.client_id = create_arguments_parser()
        self.logger.info(f'Сервер создан с параметрами {self.addr} {self.port}')
        self.clients = []
        self.messages = []

    @log
    def create_connection(self):
        try:
            self._s.bind((self.addr, self.port))
            self._s.listen(MAX_CONNECTIONS)
        except Exception as e:
            self.logger.critical(f'Сервер не подключен {e}')
            exit(1)
        finally:
            self._s.listen(MAX_CONNECTIONS)

            while True:
                try:
                    client, client_address = self._s.accept()
                except OSError:
                    pass
                else:
                    self.logger.info(f'Подключен клиент {client.fileno()} {client_address}')
                    self.clients.append(client)
                finally:
                    self.process_queue()



        # while True:
        #     client, client_address = self._s.accept()
        #     response = RESPONSE_ERROR
        #     try:
        #         data = client.recv(MAX_PACKAGE_LENGTH)
        #         if data:
        #             json_answer = data.decode(ENCODING)
        #             response = self.process_client_message(json.loads(json_answer))
        #     except:
        #         self.logger.error(f'Принято некорректное сообщение от клиента')
        #     finally:
        #         client.send(f'{response}'.encode(ENCODING))
        #         client.close()
    @log
    def read_requests(self, pending):
        responses = {}

        for client in pending:
            try:
                data = client.recv(MAX_PACKAGE_LENGTH)
                if data:
                    message = json.loads(data.decode(ENCODING))
                    print(f'message >>> ${message}')
                responses[client] = data
            except Exception as err:
                print(f'read_requests >>> ${err}')
                print('Клиент {} {} отключился'.format(client.fileno(), client.getpeername()))
                self.clients.remove(client)

        return responses

    @log
    def write_responses(self, requests, pending):
        for client in pending:
            if client in requests:
                try:
                    response = requests[client]
                    print('Отвечаем {} сообщением {}'.format(client.fileno(), response))
                    client.send(response)
                except Exception as err:
                    print(f'write_responses >>> ${err}')
                    print('Клиент {} {} отключился'.format(client.fileno(), client.getpeername()))
                    client.close()
                    self.clients.remove(client)

    @log
    def process_queue(self):
        wait = 1
        read_list = []
        write_list = []
        err_list = []
        try:
            if self.clients:
                read_list, write_list, err_list = select.select(self.clients, self.clients, [], wait)
        except OSError:
            pass

        requests = self.read_requests(read_list)
        if requests:
            self.write_responses(requests, write_list)

    # @log
    # def process_client_message(self, message):
    #     self.logger.info(f'Обработка сообщения {message}')
    #     if message['action'] == 'presence' and message['user']['account_name'] == 'GUEST':
    #         return RESPONSE_OK
    #     return RESPONSE_ERROR


def main():
    server = Server(SERVER_LOGGER)
    server.create_connection()


if __name__ == '__main__':
    main()
