"""Тесты клиента"""
import logging
import unittest
from client import Client
from log import client_log_config



class TestClass(unittest.TestCase):
    def test_not_default_account_name(self):
        client = Client(logger=logging.getLogger('client'), user='NotGuest')
        self.assertNotEqual(client.account_name, 'GUEST', 'Имя не распознано')

    def test_inst_create(self):
        client = Client(logger=logging.getLogger('client'), user='NotGuest')
        self.assertEqual(client.addr, '127.0.0.1', 'IP адрес не получен')
        self.assertEqual(client.port, 8888, 'Порт не получен')


if __name__ == '__main__':
    unittest.main()
