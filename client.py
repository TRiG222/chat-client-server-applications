# программа клиента
from socket import *
import datetime
import json
import click


@click.command()
@click.option('--addr', prompt='input ip', help='ip address server')
@click.option('--port', default=8888, prompt='port',
              help='port server.')
def form_presence(addr, port):
    s = socket(AF_INET, SOCK_STREAM)
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

    s.send(msg.encode('utf-8'))

    data = s.recv(1000000)
    print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')
    s.close()


form_presence()
