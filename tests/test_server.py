import logging
import unittest
from server import Server


class TestServer(unittest.TestCase):
    def test_inst_create(self):
        server = Server(logging.getLogger('server'))
        self.assertEqual(server.addr, '127.0.0.1', 'Адрес не получен')
        self.assertEqual(server.port, 7777, 'Порт не получен')

    def test_ok_process_client_message(self):
        server = Server(logging.getLogger('server'))
        message = {
            'action': 'presence',
            'user': {
                'account_name': 'GUEST'
            }
        }
        self.assertEqual(server.process_client_message(message), 200)

    def test_not_presence_process_client_message(self):
        server = Server(logging.getLogger('server'))
        message = {
            'action': 'quit',
            'user': {
                'account_name': 'GUEST'
            }
        }
        self.assertEqual(server.process_client_message (message), 400)

    def test_not_guest_process_client_message(self):
        server = Server(logging.getLogger('server'))
        message = {
            'action': 'presence',
            'user': {
                'account_name': 'NOTGUEST'
            }
        }
        self.assertEqual(server.process_client_message(message), 400)

    def test_empty_message_process_client_message(self):
        server = Server()
        message = {}
        self.assertRaises(KeyError, lambda: server.process_client_message(message))


if __name__ == '__main__':
    unittest.main()