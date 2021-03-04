import unittest
from socket import *
from contextlib import closing
import json


class Test_service(unittest.TestCase):

    def setUp(self):
        print('setup')
        self.server_socket = server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(('127.0.0.1', 8888))
        server_socket.listen(5)

    def tearDown(self):
        print('teardown')
        self.server_socket.close()

    def test_1(self):
        print('test1')
        self.client, self.addr = self.server_socket.accept()
        with closing(self.client) as cl:
            data = cl.recv(1000000).decode('utf-8')
            data = json.loads(data)
            self.assertEqual(data['action'], 'presence')
            cl.send('succes test'.encode('ascii'))

