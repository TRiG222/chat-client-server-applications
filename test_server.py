import unittest
from socket import *


class Test_service(unittest.TestCase):

    def setUp(self):
        print('setup')
        self.client_socket = client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 8888))

    def tearDown(self):
        print('teardown')
        self.client_socket.close()

    def test_1(self):
        print('test1')
        self.client_socket.send('message1'.encode())
        self.assertEqual(self.client_socket.recv(1024).decode(), 'reply1')

    def test_2(self):
        print('test2')
        self.client_socket.send('message2'.encode())
        self.assertEqual(self.client_socket.recv(1024).decode(), 'reply2')