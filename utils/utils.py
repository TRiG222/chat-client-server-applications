"""Утилиты"""
import argparse
import json
from time import time
from utils.config import DEFAULT_IP_ADDRESS, DEFAULT_PORT, DICT_ANSWER_CODE, ENCODING, DEFAULT_CLIENT_ID, PRESENCE


class Message:
    def __init__(self, action, message_time=time()):
        self.action = action
        self.time = message_time

    def __str__(self):
        return f'message >>> {self.action}'

    def to_bytes(self):
        json_message = json.dumps(self.serialize())
        encoded_message = json_message.encode(ENCODING)
        return encoded_message

    def serialize(self):
        return {
            'action': self.action,
            'time': self.time
        }


class PresenceMessage(Message):
    def __init__(self, user=None):
        super().__init__(action=PRESENCE)
        self.user = user

    def serialize(self):
        _pr = super().serialize()
        _pr['user'] = self.user
        return _pr


# class NonPresenceMessage(Message):
#     def __init__(self, user=None):
#         super().__init__(action=NON_PRESENCE)
#         self.user = user
#
#     def serialize(self):
#         _pr = super().serialize()
#         _pr['user'] = self.user
#         return _pr

class ChatMessage(Message):
    def __init__(self, user=None, text=None):
        super().__init__(action=CHAT)
        self.user = user
        self.text = text

    def serialize(self):
        _pr = super().serialize()
        _pr['user'] = self.user
        _pr['text'] = self.text
        return _pr


class Response:
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f'[{self.get_code()}] {self.get_message()}'

    def get_code(self):
        if self.response:
            return int(self.response)
        return 0

    def get_message(self):
        return f'{DICT_ANSWER_CODE[self.get_code()]}'

    def serialize(self):
        return {
            'response': self.response
        }

    def to_bytes(self):
        json_response = json.dumps(self.serialize())
        encoded_message = json_response.encode(ENCODING)
        return encoded_message


def create_arguments_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a',  type=str, default=DEFAULT_IP_ADDRESS)
    parser.add_argument('-p',  type=int, default=DEFAULT_PORT)
    parser.add_argument('-n', type=str, default='')
    args = parser.parse_args()

    try:
        client_id = args.id
        addr = parser.parse_args().addr
        port = parser.parse_args().port
        if port < 1024 or port > 65535:
            raise
    except:
        client_id = DEFAULT_CLIENT_ID
        addr = DEFAULT_IP_ADDRESS
        port = DEFAULT_PORT
        print(f'Неверные параметры, применены стандартные: IP {DEFAULT_IP_ADDRESS}, port {DEFAULT_PORT}')

    return addr, port, client_id
