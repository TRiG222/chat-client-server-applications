# программа клиента
from socket import *
import datetime
import json
import click

ENCODING = 'UTF-8'


@click.command()
@click.option('--addr', prompt='input ip', help='ip address server')
@click.option('--port', default=8888, prompt='port',
              help='port server.')
def form_presence(addr, port):

    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((addr, port))

        msg = {
            "action": "presence",
            "time": f'{datetime.date.today()}',
            "type": "status",
            "user": {
                "account_name": "C0deMaver1ck",
                "status": "Yep, I am here!"
            }
        }

        msg = json.dumps(msg)

        s.send(msg.encode(ENCODING))

        data = s.recv(1000000)
        print('Сообщение от сервера: ', data.decode(ENCODING), ', длиной ', len(data), ' байт')



form_presence()
